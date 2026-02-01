"""
UWM API endpoints.
"""
from fastapi import APIRouter, Depends, status

try:
    from app.server.dependencies.auth import get_current_user
    from app.server.models.user import User
    from app.server.schemas.uwm import UWMTestConnectionResponse
    from app.server.services.uwm_auth_service import UWMAuthService
except ModuleNotFoundError:
    from dependencies.auth import get_current_user
    from models.user import User
    from schemas.uwm import UWMTestConnectionResponse
    from services.uwm_auth_service import UWMAuthService


router = APIRouter(prefix="/uwm", tags=["uwm"])


@router.post(
    "/test-connection",
    response_model=UWMTestConnectionResponse,
    status_code=status.HTTP_200_OK,
    summary="Test UWM API connection",
    description="Test the UWM OAuth connection and return detailed results including logs."
)
async def test_uwm_connection(
    current_user: User = Depends(get_current_user),
):
    """Test UWM API connection using configured credentials."""
    # Create a fresh instance for isolated testing (don't use singleton)
    uwm_service = UWMAuthService()

    try:
        result = await uwm_service.test_connection()
        return UWMTestConnectionResponse(**result)
    finally:
        # Clean up the service connection
        uwm_service.disconnect()
