"""
User API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

try:
    from app.server.database import get_db
    from app.server.dependencies.auth import get_current_user
    from app.server.models.user import User
    from app.server.schemas.user import UserProfile, UserUpdate, UserResponse
    from app.server.services.user_service import user_service
except ModuleNotFoundError:
    from database import get_db
    from dependencies.auth import get_current_user
    from models.user import User
    from schemas.user import UserProfile, UserUpdate, UserResponse
    from services.user_service import user_service


router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/me",
    response_model=UserProfile,
    summary="Get current user profile",
    description="Get complete user profile with tenant, role, permissions, and available modules."
)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user profile."""
    user_profile = await user_service.get_user_profile(current_user.id, db)

    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )

    return user_profile


@router.patch(
    "/me",
    response_model=UserResponse,
    summary="Update current user profile",
    description="Update user profile information (first name, last name)."
)
async def update_current_user_profile(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update current user profile."""
    updated_user = await user_service.update_user(current_user.id, data, db)

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return updated_user
