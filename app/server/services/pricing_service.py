"""
Pricing service for UWM API integration.

Provides instant price quotes from UWM API with OAuth authentication,
field mapping, and rate limiting handling.
"""
import asyncio
import logging
from typing import Any

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

try:
    from app.server.config import settings
    from app.server.models.pricing_quote import PricingQuote
    from app.server.schemas.pricing_quote import PricingQuoteRequest
    from app.server.services.uwm_auth_service import uwm_auth_service
    from app.server.services.uwm_field_mapper import uwm_field_mapper
except ModuleNotFoundError:
    from config import settings
    from models.pricing_quote import PricingQuote
    from schemas.pricing_quote import PricingQuoteRequest
    from services.uwm_auth_service import uwm_auth_service
    from services.uwm_field_mapper import uwm_field_mapper

logger = logging.getLogger(__name__)

# Rate limit retry configuration
MAX_RATE_LIMIT_RETRIES = 3
RATE_LIMIT_WAIT_SECONDS = 30


class PricingService:
    """Service for UWM pricing API integration."""

    def __init__(self):
        """Initialize pricing service configuration."""
        self.api_url = settings.uwm_api_url
        self.timeout = settings.uwm_api_timeout
        self.use_real_api = settings.uwm_use_real_api
        self.proxy_url = settings.uwm_proxy_url

    def _get_http_client(self) -> httpx.AsyncClient:
        """Get httpx client with optional SOCKS proxy support (development only)."""
        # Only use proxy in development environment
        if self.proxy_url and settings.environment == "development":
            logger.debug(f"Using proxy for UWM API (development): {self.proxy_url}")
            return httpx.AsyncClient(timeout=self.timeout, proxy=self.proxy_url)
        return httpx.AsyncClient(timeout=self.timeout)

    async def get_instant_price_quote(
        self,
        request_data: PricingQuoteRequest,
        customer_id: int,
        user_id: int,
        tenant_id: int,
        db: AsyncSession,
        client_ip: str | None = None,
        request_url: str | None = None
    ) -> PricingQuote:
        """
        Request an instant price quote from UWM API.

        Args:
            request_data: Pricing quote request parameters
            customer_id: Customer ID
            user_id: User ID making the request
            tenant_id: Tenant ID for scoping
            db: Database session
            client_ip: Client IP address of the request sender
            request_url: Full request URL with query parameters

        Returns:
            Created PricingQuote instance with full response

        Raises:
            ValueError: If API request fails or returns invalid data
        """
        # Store original request params for debugging (includes camelCase UWM fields)
        request_params = {
            # Internal snake_case fields
            "loan_type": request_data.loan_type,
            "loan_amount": request_data.loan_amount,
            "property_value": request_data.property_value,
            "credit_score": request_data.credit_score or request_data.creditScore,
            "loan_purpose": request_data.loan_purpose,
            "property_type": request_data.property_type,
            "occupancy": request_data.occupancy,
            "state": request_data.state,
            "county": request_data.county,
            "zip_code": request_data.zip_code or request_data.propertyZipCode,
            "lock_period": request_data.lock_period,
            "dti_ratio": request_data.dti_ratio,
            "first_time_buyer": request_data.first_time_buyer if request_data.first_time_buyer is not None else request_data.firstTimeHomeBuyer,
            "number_of_units": request_data.number_of_units,
            "broker_alias": request_data.broker_alias or request_data.brokerAlias,
            "borrower_name": request_data.borrower_name or request_data.borrowerName,
            "monthly_income": request_data.monthly_income or request_data.monthlyIncome,
            "sales_price": request_data.sales_price if request_data.sales_price is not None else request_data.salesPrice,
            # UWM camelCase fields (passed through from client)
            "loanAmount": request_data.loanAmount,
            "loanTypeIds": request_data.loanTypeIds,
            "appraisedValue": request_data.appraisedValue,
            "purposeTypeId": request_data.purposeTypeId,
            "propertyTypeId": request_data.propertyTypeId,
            "occupancyTypeId": request_data.occupancyTypeId,
        }

        # Derive loan_type from UWM config if not provided
        loan_type = request_data.loan_type or "uwm_direct"

        logger.info(f"Requesting price quote for customer {customer_id}")

        if self.use_real_api:
            # Use real UWM API
            full_response, uwm_payload = await self._call_uwm_api(request_data, customer_id)
        else:
            # Use mock response for development
            full_response = self._generate_mock_response(request_data, customer_id, user_id)
            uwm_payload = None

        # Extract best price and scenario ID from response
        best_price = full_response.get("best_price", "N/A")
        uwm_scenario_id = full_response.get("uwm_scenario_id")

        logger.info(f"Received price quote for customer {customer_id}: best_price={best_price}")

        # Save quote to database with all metadata
        pricing_quote = PricingQuote(
            customer_id=customer_id,
            user_id=user_id,
            tenant_id=tenant_id,
            loan_type=loan_type,
            best_price=best_price,
            full_response=full_response,
            uwm_scenario_id=uwm_scenario_id,
            uwm_request_payload=uwm_payload,
            request_params=request_params,
            client_ip=client_ip,
            request_url=request_url,
        )

        db.add(pricing_quote)
        await db.commit()
        await db.refresh(pricing_quote)

        logger.info(f"Saved pricing quote {pricing_quote.id} for customer {customer_id}")

        return pricing_quote

    async def _call_uwm_api(
        self,
        request_data: PricingQuoteRequest,
        customer_id: int,
        retry_count: int = 0
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """
        Call the real UWM API with OAuth authentication.

        Args:
            request_data: Pricing quote request parameters
            customer_id: Customer ID for logging
            retry_count: Current retry attempt for rate limiting

        Returns:
            Tuple of (internal_response, uwm_request_payload)

        Raises:
            ValueError: If API request fails
        """
        # Load UWM payload from JSON config file
        import json
        import os
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uwm_config.json')
        with open(config_path, 'r') as f:
            uwm_payload = json.load(f)

        logger.debug(f"UWM API request payload for customer {customer_id}: {uwm_payload}")

        try:
            # Get OAuth token
            auth_headers = await uwm_auth_service.get_authorization_header()

            async with self._get_http_client() as client:
                headers = {
                    **auth_headers,
                    "Content-Type": "application/json",
                }

                response = await client.post(
                    self.api_url,
                    json=uwm_payload,
                    headers=headers,
                )

                # Handle rate limiting (429)
                if response.status_code == 429:
                    if retry_count < MAX_RATE_LIMIT_RETRIES:
                        logger.warning(
                            f"UWM API rate limited for customer {customer_id}, "
                            f"waiting {RATE_LIMIT_WAIT_SECONDS}s (attempt {retry_count + 1}/{MAX_RATE_LIMIT_RETRIES})"
                        )
                        await asyncio.sleep(RATE_LIMIT_WAIT_SECONDS)
                        return await self._call_uwm_api(request_data, customer_id, retry_count + 1)
                    else:
                        raise ValueError(
                            "UWM API rate limit exceeded. Please try again later."
                        )

                # Handle unauthorized (401) - clear token cache and retry once
                if response.status_code == 401 and retry_count == 0:
                    logger.warning(
                        f"UWM API unauthorized for customer {customer_id}, "
                        "clearing token cache and retrying"
                    )
                    uwm_auth_service.clear_cached_tokens()
                    return await self._call_uwm_api(request_data, customer_id, retry_count + 1)

                # Handle other errors
                if response.status_code >= 400:
                    error_detail = self._parse_uwm_error(response)
                    logger.error(
                        f"UWM API error for customer {customer_id}: "
                        f"{response.status_code} - {error_detail}"
                    )
                    raise ValueError(f"UWM API error: {error_detail}")

                # Parse successful response
                uwm_response = response.json()
                logger.debug(f"UWM API raw response: {uwm_response}")

                # Convert UWM response to internal format
                internal_response = uwm_field_mapper.from_uwm_response(uwm_response)

                return internal_response, uwm_payload

        except httpx.TimeoutException as e:
            logger.error(f"UWM API timeout for customer {customer_id}: {e}")
            raise ValueError(
                "UWM API request timed out. Please try again later."
            ) from e
        except httpx.RequestError as e:
            logger.error(f"UWM API network error for customer {customer_id}: {e}")
            raise ValueError(
                "Unable to connect to UWM API. Please check your network connection."
            ) from e

    def _parse_uwm_error(self, response: httpx.Response) -> str:
        """Parse error response from UWM API."""
        try:
            error_data = response.json()
            if "error" in error_data:
                error_msg = error_data.get("error", {})
                if isinstance(error_msg, dict):
                    return error_msg.get("message", str(error_msg))
                return str(error_msg)
            if "message" in error_data:
                return error_data["message"]
            return str(error_data)
        except Exception:
            return f"HTTP {response.status_code}: {response.text[:200]}"

    def _generate_mock_response(
        self,
        request_data: PricingQuoteRequest,
        customer_id: int,
        user_id: int
    ) -> dict[str, Any]:
        """
        Generate a mock UWM API response for development.

        This method is used when UWM_USE_REAL_API is False.

        Args:
            request_data: Request parameters to base mock response on
            customer_id: Customer ID
            user_id: User ID

        Returns:
            Mock API response in internal format
        """
        # Load UWM config for default values
        import json
        import os
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uwm_config.json')
        with open(config_path, 'r') as f:
            uwm_config = json.load(f)

        # Extract values with fallback to UWM config
        loan_amount_str = request_data.loanAmount or uwm_config.get("loanAmount", "320000")
        loan_amount = float(loan_amount_str)
        property_value = request_data.appraisedValue or request_data.property_value or uwm_config.get("appraisedValue", 450000)
        credit_score = request_data.creditScore or request_data.credit_score or uwm_config.get("creditScore", 720)
        loan_type = request_data.loan_type or "uwm_direct"
        lock_period = request_data.lock_period or 30

        ltv_ratio = (loan_amount / property_value) * 100

        # Mock rate calculation (simplified)
        base_rate = 6.25
        if credit_score >= 760:
            base_rate -= 0.5
        elif credit_score < 680:
            base_rate += 0.75

        if loan_type == "fha":
            base_rate += 0.25
        elif loan_type == "va":
            base_rate -= 0.125

        if ltv_ratio > 80:
            base_rate += 0.25

        rate = round(base_rate, 3)
        apr = round(rate + 0.15, 3)

        # Calculate monthly payment (simplified P&I only)
        monthly_rate = rate / 100 / 12
        num_payments = 360  # 30-year mortgage
        if monthly_rate > 0:
            monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
        else:
            monthly_payment = loan_amount / num_payments

        # Generate mock scenario ID
        mock_scenario_id = f"mock-{customer_id}-{user_id}-{int(loan_amount)}"

        return {
            "best_price": f"${monthly_payment:,.2f}/mo",
            "rate": rate,
            "apr": apr,
            "monthly_payment": monthly_payment,
            "uwm_scenario_id": mock_scenario_id,
            "product_name": "30 Year Fixed",
            "lock_period": lock_period,
            "points": 0,
            "lender_credit": 0,
            "closing_costs": round(loan_amount * 0.02, 2),
            "total_cash_to_close": round(property_value * 0.03 + loan_amount * 0.02, 2),
            "valid_quote_count": 3,
            "invalid_quote_count": 0,
            "valid_quotes": [
                {
                    "productName": "30 Year Fixed",
                    "rate": rate,
                    "apr": apr,
                    "price": 100.0,
                    "monthlyPayment": monthly_payment,
                    "points": 0,
                    "lenderCredit": 0,
                    "lockPeriod": lock_period,
                },
                {
                    "productName": "30 Year Fixed - Discounted",
                    "rate": rate - 0.125,
                    "apr": apr - 0.125,
                    "price": 99.5,
                    "monthlyPayment": monthly_payment * 0.99,
                    "points": 0.5,
                    "lenderCredit": 0,
                    "lockPeriod": lock_period,
                },
                {
                    "productName": "30 Year Fixed - No Cost",
                    "rate": rate + 0.375,
                    "apr": apr + 0.375,
                    "price": 101.5,
                    "monthlyPayment": monthly_payment * 1.02,
                    "points": -1.5,
                    "lenderCredit": loan_amount * 0.015,
                    "lockPeriod": lock_period,
                },
            ],
            "invalid_quotes": [],
            "loan_details": {
                "loan_amount": loan_amount,
                "property_value": property_value,
                "ltv": round(ltv_ratio, 2),
                "credit_score": credit_score,
                "loan_type": loan_type,
                "loan_purpose": request_data.loan_purpose or "purchase",
            },
            "is_mock": True,
        }


# Singleton instance
pricing_service = PricingService()
