import logging

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import check_database_connection
from routers import auth_router, users_router, customers_router, pricing_router, uwm_router
from services.rate_limit_service import rate_limit_service

# Load .env for local development
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Valargen API",
    description="Mortgage automation platform with comprehensive authentication",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_url,
        "http://localhost",
        "http://localhost:80",
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("Starting Valargen API...")
    logger.info("Rate limiting service initialized" if rate_limit_service.redis_client else "Redis unavailable - rate limiting disabled")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down Valargen API...")

    # Disconnect from Redis
    try:
        rate_limit_service.disconnect()
        logger.info("Disconnected from Redis")
    except Exception as e:
        logger.warning(f"Error disconnecting from Redis: {e}")


# Include routers
app.include_router(auth_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(customers_router, prefix="/api")
app.include_router(pricing_router, prefix="/api")
app.include_router(uwm_router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Valargen API"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    db_status = await check_database_connection()

    # Check Redis connection
    redis_status = "connected" if rate_limit_service.redis_client else "disconnected"

    return {
        **db_status,
        "redis": redis_status,
        "api": "healthy"
    }


@app.get("/api/health")
async def api_health():
    """API health check endpoint."""
    return await health_check()
