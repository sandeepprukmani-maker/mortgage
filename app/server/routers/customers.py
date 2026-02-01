"""
Customer API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

try:
    from app.server.database import get_db
    from app.server.dependencies.auth import get_current_user
    from app.server.models.user import User
    from app.server.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse, CustomerList
    from app.server.services.customer_service import customer_service
except ModuleNotFoundError:
    from database import get_db
    from dependencies.auth import get_current_user
    from models.user import User
    from schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse, CustomerList
    from services.customer_service import customer_service


router = APIRouter(prefix="/customers", tags=["customers"])


@router.post(
    "",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new customer",
    description="Create a new customer record for the current user's tenant."
)
async def create_customer(
    data: CustomerCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new customer."""
    try:
        customer = await customer_service.create_customer(
            data=data,
            tenant_id=current_user.tenant_id,
            db=db
        )
        return customer
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "",
    response_model=CustomerList,
    summary="List customers",
    description="Get a list of all customers for the current user's tenant."
)
async def list_customers(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all customers for the current tenant."""
    customers = await customer_service.list_customers(
        tenant_id=current_user.tenant_id,
        db=db,
        skip=skip,
        limit=limit
    )
    return CustomerList(customers=customers, total=len(customers))


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
    summary="Get customer by ID",
    description="Get a single customer by ID. Customer must belong to the current user's tenant."
)
async def get_customer(
    customer_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a single customer by ID."""
    customer = await customer_service.get_customer(
        customer_id=customer_id,
        tenant_id=current_user.tenant_id,
        db=db
    )

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    return customer


@router.patch(
    "/{customer_id}",
    response_model=CustomerResponse,
    summary="Update customer",
    description="Update customer information. Customer must belong to the current user's tenant."
)
async def update_customer(
    customer_id: int,
    data: CustomerUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a customer."""
    try:
        customer = await customer_service.update_customer(
            customer_id=customer_id,
            data=data,
            tenant_id=current_user.tenant_id,
            db=db
        )

        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )

        return customer
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
