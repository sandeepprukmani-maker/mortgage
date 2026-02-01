"""
Authentication API endpoints.
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, Response, status, Cookie
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

try:
    from app.server.config import settings
    from app.server.database import get_db
    from app.server.schemas.auth import (
        RegisterRequest,
        LoginRequest,
        ForgotPasswordRequest,
        ResetPasswordRequest,
        AuthResponse,
        MessageResponse,
    )
    from app.server.schemas.token import TokenResponse
    from app.server.services.auth_service import auth_service
    from app.server.services.oauth_service import oauth_service
except ModuleNotFoundError:
    from config import settings
    from database import get_db
    from schemas.auth import (
        RegisterRequest,
        LoginRequest,
        ForgotPasswordRequest,
        ResetPasswordRequest,
        AuthResponse,
        MessageResponse,
    )
    from schemas.token import TokenResponse
    from services.auth_service import auth_service
    from services.oauth_service import oauth_service


router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Register a new user with email and password. Returns success message without auto-login."
)
async def register(
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user."""
    try:
        await auth_service.register_user(data, db)
        return AuthResponse(
            message="Registration successful. Please login to continue.",
            user=None
        )
    except ValueError as e:
        if "already" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login with email and password",
    description="Authenticate user and return access token. Refresh token set in HTTPOnly cookie."
)
async def login(
    data: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    """Login user with email and password."""
    try:
        access_token, refresh_token, user = await auth_service.login_user(
            data.email,
            data.password,
            db
        )

        # Set refresh token in HTTPOnly cookie
        response.set_cookie(
            key="refresh_token",
            value=refresh_token.token,
            httponly=True,
            secure=settings.cookie_secure,
            samesite=settings.cookie_samesite,
            max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
            path="/"
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60
        )

    except ValueError as e:
        error_msg = str(e)
        if "locked" in error_msg.lower() or "too many" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=error_msg
            )
        # Check for auth provider mismatch (wrong authentication method)
        if "uses" in error_msg.lower() and "authentication" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_msg
        )


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="Logout user",
    description="Revoke refresh token and clear cookie."
)
async def logout(
    response: Response,
    refresh_token: str = Cookie(None),
    db: AsyncSession = Depends(get_db)
):
    """Logout user by revoking refresh token."""
    if refresh_token:
        try:
            await auth_service.logout_user(refresh_token, db)
        except ValueError:
            # Token already invalid, ignore
            pass

    # Clear refresh token cookie
    response.delete_cookie(
        key="refresh_token",
        path="/",
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite
    )

    return MessageResponse(message="Successfully logged out")


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token",
    description="Get new access token using refresh token from cookie. Implements token rotation."
)
async def refresh(
    response: Response,
    refresh_token: str = Cookie(None),
    db: AsyncSession = Depends(get_db)
):
    """Refresh access token using refresh token."""
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found"
        )

    try:
        new_access_token, new_refresh_token = await auth_service.refresh_access_token(
            refresh_token,
            db
        )

        # Set new refresh token in cookie
        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token.token,
            httponly=True,
            secure=settings.cookie_secure,
            samesite=settings.cookie_samesite,
            max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
            path="/"
        )

        return TokenResponse(
            access_token=new_access_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.get(
    "/google",
    summary="Get Google OAuth authorization URL",
    description="Returns authorization URL to redirect user to Google OAuth consent screen."
)
async def google_auth():
    """Get Google OAuth authorization URL."""
    # Check if OAuth is configured before starting the flow
    if not oauth_service.is_configured():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google Sign-In is not available. OAuth credentials not configured."
        )

    try:
        auth_url = oauth_service.get_google_authorization_url()
        return {"authorization_url": auth_url}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )


@router.get(
    "/google/callback",
    summary="Google OAuth callback",
    description="Handle OAuth callback from Google and authenticate/register user."
)
async def google_callback(
    code: str = None,
    state: str = None,
    error: str = None,
    db: AsyncSession = Depends(get_db)
):
    """Handle Google OAuth callback."""
    # Handle OAuth errors from Google
    if error:
        error_params = urlencode({"error": error})
        return RedirectResponse(
            url=f"{settings.frontend_url}/oauth/callback?{error_params}",
            status_code=status.HTTP_302_FOUND
        )

    if not code:
        error_params = urlencode({"error": "Authorization code not provided"})
        return RedirectResponse(
            url=f"{settings.frontend_url}/oauth/callback?{error_params}",
            status_code=status.HTTP_302_FOUND
        )

    try:
        access_token, refresh_token, user = await auth_service.login_with_google(
            code,
            db
        )

        # Build redirect URL with token
        redirect_url = f"{settings.frontend_url}/oauth/callback?access_token={access_token}"

        # Create redirect response and set cookie
        response = RedirectResponse(
            url=redirect_url,
            status_code=status.HTTP_302_FOUND
        )

        # Set refresh token in HTTPOnly cookie
        response.set_cookie(
            key="refresh_token",
            value=refresh_token.token,
            httponly=True,
            secure=settings.cookie_secure,
            samesite=settings.cookie_samesite,
            max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
            path="/"
        )

        return response

    except ValueError as e:
        # ValueError contains user-friendly messages from oauth_service
        error_params = urlencode({"error": str(e)})
        return RedirectResponse(
            url=f"{settings.frontend_url}/oauth/callback?{error_params}",
            status_code=status.HTTP_302_FOUND
        )
    except Exception as e:
        # Log the full error for debugging, but return generic message to user
        logger.error(f"Unexpected OAuth error: {type(e).__name__}: {e}")
        error_params = urlencode({
            "error": "An unexpected error occurred during sign-in. Please try again."
        })
        return RedirectResponse(
            url=f"{settings.frontend_url}/oauth/callback?{error_params}",
            status_code=status.HTTP_302_FOUND
        )


@router.post(
    "/forgot-password",
    response_model=MessageResponse,
    summary="Request password reset",
    description="Send password reset email (logged to console in MVP). Always returns success to prevent email enumeration."
)
async def forgot_password(
    data: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db)
):
    """Request password reset."""
    await auth_service.request_password_reset(data.email, db)

    # Always return success message
    return MessageResponse(
        message="If an account exists with this email, a password reset link has been sent."
    )


@router.post(
    "/reset-password",
    response_model=MessageResponse,
    summary="Reset password",
    description="Reset user password using reset token."
)
async def reset_password(
    data: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db)
):
    """Reset user password."""
    try:
        await auth_service.reset_password(data.token, data.new_password, db)
        return MessageResponse(message="Password reset successful. Please login with your new password.")

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
