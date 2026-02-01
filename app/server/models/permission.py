"""
Permission model for role-based access control.
"""
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Table, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base

if TYPE_CHECKING:
    from models.role import Role


# Many-to-many association table for roles and permissions
RolePermission = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True),
)


class Permission(Base):
    """Permission model for granular access control."""

    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        comment="Permission name (e.g., 'view_loans', 'edit_loans')"
    )
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    module: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Module this permission belongs to (e.g., 'loans', 'borrowers')"
    )

    # Relationships
    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary=RolePermission,
        back_populates="permissions"
    )

    def __repr__(self) -> str:
        return f"<Permission(id={self.id}, name='{self.name}', module='{self.module}')>"
