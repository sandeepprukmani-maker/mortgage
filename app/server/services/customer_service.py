"""
Customer management service.
"""
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

try:
    from app.server.models.customer import Customer
    from app.server.schemas.customer import CustomerCreate, CustomerUpdate
except ModuleNotFoundError:
    from models.customer import Customer
    from schemas.customer import CustomerCreate, CustomerUpdate


class CustomerService:
    """Service for customer management operations."""

    async def create_customer(
        self,
        data: CustomerCreate,
        tenant_id: int,
        db: AsyncSession
    ) -> Customer:
        """
        Create a new customer.

        Args:
            data: Customer creation data
            tenant_id: Tenant ID to associate customer with
            db: Database session

        Returns:
            Created Customer instance

        Raises:
            ValueError: If validation fails
        """
        # Create customer
        customer = Customer(
            name=data.name,
            email=data.email,
            phone=data.phone,
            company_name=data.company_name,
            tenant_id=tenant_id
        )

        db.add(customer)
        await db.commit()
        await db.refresh(customer)

        return customer

    async def get_customer(
        self,
        customer_id: int,
        tenant_id: int,
        db: AsyncSession
    ) -> Optional[Customer]:
        """
        Get a customer by ID with tenant scoping.

        Args:
            customer_id: Customer ID
            tenant_id: Tenant ID for security scoping
            db: Database session

        Returns:
            Customer instance or None if not found
        """
        result = await db.execute(
            select(Customer)
            .where(Customer.id == customer_id)
            .where(Customer.tenant_id == tenant_id)
        )
        return result.scalar_one_or_none()

    async def list_customers(
        self,
        tenant_id: int,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> list[Customer]:
        """
        List all customers for a tenant with pagination.

        Args:
            tenant_id: Tenant ID for security scoping
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Customer instances
        """
        result = await db.execute(
            select(Customer)
            .where(Customer.tenant_id == tenant_id)
            .order_by(Customer.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def update_customer(
        self,
        customer_id: int,
        data: CustomerUpdate,
        tenant_id: int,
        db: AsyncSession
    ) -> Optional[Customer]:
        """
        Update a customer.

        Args:
            customer_id: Customer ID
            data: Customer update data
            tenant_id: Tenant ID for security scoping
            db: Database session

        Returns:
            Updated Customer instance or None if not found

        Raises:
            ValueError: If validation fails
        """
        # Get customer with tenant scoping
        customer = await self.get_customer(customer_id, tenant_id, db)
        if not customer:
            return None

        # Update fields if provided
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(customer, field, value)

        await db.commit()
        await db.refresh(customer)

        return customer


# Singleton instance
customer_service = CustomerService()
