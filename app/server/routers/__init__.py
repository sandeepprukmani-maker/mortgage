"""
API routers for Valargen application.
"""
from routers.auth import router as auth_router
from routers.users import router as users_router
from routers.customers import router as customers_router
from routers.pricing import router as pricing_router
from routers.uwm import router as uwm_router

__all__ = [
    "auth_router",
    "users_router",
    "customers_router",
    "pricing_router",
    "uwm_router",
]
