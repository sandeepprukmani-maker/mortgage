"""
PricingQuote model for storing pricing quote responses.
"""
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

from sqlalchemy import String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base

if TYPE_CHECKING:
    from models.customer import Customer
    from models.user import User
    from models.tenant import Tenant


class PricingQuote(Base):
    """PricingQuote model for storing pricing quote responses."""

    __tablename__ = "pricing_quotes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Foreign keys
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Quote details
    loan_type: Mapped[str] = mapped_column(String(50), nullable=False)
    best_price: Mapped[str] = mapped_column(String(100), nullable=False)

    # Store full API response as JSONB
    full_response: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)

    # UWM API integration fields
    uwm_scenario_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
        comment="UWM scenario identifier for quote tracking"
    )
    uwm_request_payload: Mapped[dict[str, Any] | None] = mapped_column(
        JSON,
        nullable=True,
        comment="Original request payload sent to UWM API"
    )
    request_params: Mapped[dict[str, Any] | None] = mapped_column(
        JSON,
        nullable=True,
        comment="Internal request parameters before UWM mapping"
    )

    # Request metadata
    client_ip: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True,
        comment="Client IP address of the request sender"
    )
    request_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        comment="Full request URL with query parameters"
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    customer: Mapped["Customer"] = relationship("Customer", back_populates="pricing_quotes")
    user: Mapped["User"] = relationship("User", back_populates="pricing_quotes")
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="pricing_quotes")

    def __repr__(self) -> str:
        return f"<PricingQuote(id={self.id}, customer_id={self.customer_id}, best_price='{self.best_price}')>"
