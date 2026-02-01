"""
Pricing quote-related Pydantic schemas.
"""
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class PricingQuoteRequest(BaseModel):
    """Schema for requesting a pricing quote.

    The actual UWM payload is loaded from uwm_config.json on the server.
    Client only needs to provide customer_id. Other fields are optional
    and used for logging/tracking purposes.
    """

    customer_id: int = Field(..., description="Customer ID to request quote for")

    # Internal fields - all optional since UWM config is loaded from server JSON
    loan_type: str | None = Field(default=None, description="Loan type for internal tracking")
    loan_amount: float | None = Field(default=None, description="Loan amount for internal tracking")
    property_value: float | None = Field(default=None, description="Property value for internal tracking")
    credit_score: int | None = Field(default=None, description="Credit score for internal tracking")
    loan_purpose: str | None = Field(default=None, description="Loan purpose for internal tracking")
    property_type: str | None = Field(default=None, description="Property type for internal tracking")
    occupancy: str | None = Field(default=None, description="Occupancy for internal tracking")
    state: str | None = Field(default=None, description="Property state for internal tracking")
    county: str | None = Field(default=None, description="Property county name")
    zip_code: str | None = Field(default=None, description="Property ZIP code")
    lock_period: int | None = Field(default=None, description="Rate lock period in days")
    dti_ratio: float | None = Field(default=None, description="Debt-to-income ratio")
    first_time_buyer: bool | None = Field(default=None, description="First-time homebuyer flag")
    number_of_units: int | None = Field(default=None, description="Number of units (1-4)")
    broker_alias: str | None = Field(default=None, description="UWM broker alias")
    borrower_name: str | None = Field(default=None, description="Borrower name")
    monthly_income: float | None = Field(default=None, description="Monthly income in dollars")
    sales_price: float | None = Field(default=None, description="Sales price")

    # UWM direct fields (camelCase) - passed through from client config
    brokerAlias: str | None = Field(default=None, description="UWM brokerAlias")
    loanAmount: str | None = Field(default=None, description="UWM loanAmount")
    loanTypeIds: list[str] | None = Field(default=None, description="UWM loanTypeIds")
    salesPrice: float | None = Field(default=None, description="UWM salesPrice")
    appraisedValue: float | None = Field(default=None, description="UWM appraisedValue")
    purposeTypeId: str | None = Field(default=None, description="UWM purposeTypeId")
    firstTimeHomeBuyer: bool | None = Field(default=None, description="UWM firstTimeHomeBuyer")
    propertyTypeId: str | None = Field(default=None, description="UWM propertyTypeId")
    occupancyTypeId: str | None = Field(default=None, description="UWM occupancyTypeId")
    propertyZipCode: str | None = Field(default=None, description="UWM propertyZipCode")
    creditScore: int | None = Field(default=None, description="UWM creditScore")
    monthlyIncome: float | None = Field(default=None, description="UWM monthlyIncome")
    borrowerName: str | None = Field(default=None, description="UWM borrowerName")

    model_config = {
        "json_schema_extra": {
            "example": {
                "customer_id": 1,
                "loan_type": "conventional",
                "loan_amount": 350000,
                "property_value": 450000,
                "credit_score": 720,
                "loan_purpose": "purchase",
                "property_type": "single-family",
                "occupancy": "primary",
                "state": "CA"
            }
        }
    }


class PricingQuoteResponse(BaseModel):
    """Schema for pricing quote response."""

    id: int
    customer_id: int
    user_id: int
    tenant_id: int
    loan_type: str
    best_price: str
    full_response: dict[str, Any]
    uwm_scenario_id: str | None = None
    uwm_request_payload: dict[str, Any] | None = None
    request_params: dict[str, Any] | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "customer_id": 1,
                "user_id": 1,
                "tenant_id": 1,
                "loan_type": "conventional",
                "best_price": "$350,000",
                "full_response": {
                    "best_price": "$350,000",
                    "rate": "6.25%",
                    "apr": "6.35%",
                    "monthly_payment": "$2,154.32",
                    "loan_id": "abc123",
                    "lock_days": 30
                },
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        }
    }
