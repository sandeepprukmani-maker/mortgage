"""
Customer-related Pydantic schemas.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class CustomerBase(BaseModel):
    """Base customer schema with common fields."""

    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=50)
    company_name: Optional[str] = Field(None, max_length=200)


class CustomerCreate(CustomerBase):
    """Schema for creating a new customer."""

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "John Smith",
                "email": "john.smith@example.com",
                "phone": "(555) 123-4567",
                "company_name": "Smith Construction LLC"
            }
        }
    }


class CustomerUpdate(BaseModel):
    """Schema for updating customer information."""

    name: Optional[str] = Field(None, min_length=1, max_length=200)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=50)
    company_name: Optional[str] = Field(None, max_length=200)

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "John Smith",
                "phone": "(555) 123-4567"
            }
        }
    }


class CustomerResponse(CustomerBase):
    """Schema for customer response."""

    id: int
    tenant_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CustomerList(BaseModel):
    """Schema for list of customers with pagination."""

    customers: list[CustomerResponse]
    total: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "customers": [
                    {
                        "id": 1,
                        "name": "John Smith",
                        "email": "john.smith@example.com",
                        "phone": "(555) 123-4567",
                        "company_name": "Smith Construction LLC",
                        "tenant_id": 1,
                        "created_at": "2024-01-01T00:00:00Z",
                        "updated_at": "2024-01-01T00:00:00Z"
                    }
                ],
                "total": 1
            }
        }
    }
