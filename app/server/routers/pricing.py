"""
Pricing API endpoints.
"""
import json
import logging
import os
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

try:
    from app.server.database import get_db
    from app.server.dependencies.auth import get_current_user
    from app.server.models.user import User
    from app.server.schemas.pricing_quote import PricingQuoteRequest, PricingQuoteResponse
    from app.server.services.pricing_service import pricing_service
    from app.server.services.customer_service import customer_service
except ModuleNotFoundError:
    from database import get_db
    from dependencies.auth import get_current_user
    from models.user import User
    from schemas.pricing_quote import PricingQuoteRequest, PricingQuoteResponse
    from services.pricing_service import pricing_service
    from services.customer_service import customer_service


router = APIRouter(prefix="/pricing", tags=["pricing"])


@router.get(
    "/config",
    summary="Get UWM config",
    description="Get the current UWM API configuration/payload template"
)
async def get_uwm_config():
    """Return UWM config from JSON file."""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uwm_config.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UWM config not found"
        )


@router.post(
    "/quote",
    response_model=PricingQuoteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Request pricing quote",
    description="Request an instant pricing quote for a non-HELOC loan product. Customer must belong to the current user's tenant."
)
async def request_pricing_quote(
    request: Request,
    data: PricingQuoteRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Request a pricing quote from UWM API."""
    # Validate customer exists and belongs to user's tenant
    customer = await customer_service.get_customer(
        customer_id=data.customer_id,
        tenant_id=current_user.tenant_id,
        db=db
    )

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found or does not belong to your organization"
        )

    # Extract client IP (handle proxy headers)
    client_ip = request.headers.get("x-forwarded-for", "").split(",")[0].strip() or request.client.host
    request_url = str(request.url)

    try:
        # Request pricing quote
        pricing_quote = await pricing_service.get_instant_price_quote(
            request_data=data,
            customer_id=data.customer_id,
            user_id=current_user.id,
            tenant_id=current_user.tenant_id,
            db=db,
            client_ip=client_ip,
            request_url=request_url
        )
        return pricing_quote
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.exception(f"Failed to request pricing quote: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to request pricing quote. Please try again later."
        )
