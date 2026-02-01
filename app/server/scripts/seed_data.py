"""
Seed initial data for Valargen database.

Run with: uv run python scripts/seed_data.py
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import select, insert

from database import AsyncSessionLocal
from models.tenant import Tenant
from models.role import Role
from models.permission import Permission, RolePermission
from models.user import User
from services.password_service import password_service


async def seed_roles():
    """Seed default roles."""
    async with AsyncSessionLocal() as db:
        # Check if roles already exist
        result = await db.execute(select(Role))
        existing_roles = result.scalars().all()

        if existing_roles:
            print("Roles already exist, skipping...")
            return

        # Create roles
        roles = [
            Role(
                name="loan_officer",
                description="Loan Officer with access to loan management and borrower information"
            ),
            Role(
                name="admin",
                description="Administrator with elevated privileges for user and system management"
            ),
            Role(
                name="super_admin",
                description="Super Administrator with full system access"
            ),
        ]

        for role in roles:
            db.add(role)

        await db.commit()
        print(f"Created {len(roles)} roles")


async def seed_permissions():
    """Seed default permissions."""
    async with AsyncSessionLocal() as db:
        # Check if permissions already exist
        result = await db.execute(select(Permission))
        existing_permissions = result.scalars().all()

        if existing_permissions:
            print("Permissions already exist, skipping...")
            return

        # Create permissions
        permissions = [
            # Dashboard
            Permission(name="view_dashboard", description="View dashboard", module="dashboard"),

            # Loans
            Permission(name="view_loans", description="View loans", module="loans"),
            Permission(name="create_loans", description="Create new loans", module="loans"),
            Permission(name="edit_loans", description="Edit existing loans", module="loans"),
            Permission(name="delete_loans", description="Delete loans", module="loans"),

            # Borrowers
            Permission(name="view_borrowers", description="View borrowers", module="borrowers"),
            Permission(name="create_borrowers", description="Create new borrowers", module="borrowers"),
            Permission(name="edit_borrowers", description="Edit borrower information", module="borrowers"),
            Permission(name="delete_borrowers", description="Delete borrowers", module="borrowers"),

            # Documents
            Permission(name="view_documents", description="View documents", module="documents"),
            Permission(name="upload_documents", description="Upload new documents", module="documents"),
            Permission(name="download_documents", description="Download documents", module="documents"),
            Permission(name="delete_documents", description="Delete documents", module="documents"),

            # Analytics
            Permission(name="view_analytics", description="View analytics and reports", module="analytics"),
            Permission(name="export_analytics", description="Export analytics data", module="analytics"),

            # Automation
            Permission(name="view_automation", description="View automation workflows", module="automation"),
            Permission(name="manage_automation", description="Create and manage automation workflows", module="automation"),

            # User Management (admin only)
            Permission(name="view_users", description="View user list", module="admin"),
            Permission(name="manage_users", description="Create, edit, and delete users", module="admin"),
            Permission(name="manage_roles", description="Manage roles and permissions", module="admin"),
        ]

        for permission in permissions:
            db.add(permission)

        await db.commit()
        print(f"Created {len(permissions)} permissions")


async def assign_role_permissions():
    """Assign permissions to roles."""
    async with AsyncSessionLocal() as db:
        # Check if role permissions already exist (use select from Table directly)
        result = await db.execute(select(RolePermission))
        existing = result.first()

        if existing:
            print("Role permissions already assigned, skipping...")
            return

        # Get roles
        result = await db.execute(select(Role))
        roles = {role.name: role for role in result.scalars().all()}

        # Get permissions
        result = await db.execute(select(Permission))
        all_permissions = result.scalars().all()
        permissions_by_name = {p.name: p for p in all_permissions}

        # Loan Officer permissions (basic access)
        loan_officer_perms = [
            "view_dashboard",
            "view_loans", "create_loans", "edit_loans",
            "view_borrowers", "create_borrowers", "edit_borrowers",
        ]

        # Admin permissions (all except super admin functions)
        admin_perms = [p.name for p in all_permissions if p.name != "manage_roles"]

        # Super Admin permissions (everything)
        super_admin_perms = [p.name for p in all_permissions]

        # Assign permissions using insert() for Table objects
        for perm_name in loan_officer_perms:
            if perm_name in permissions_by_name:
                await db.execute(
                    insert(RolePermission).values(
                        role_id=roles["loan_officer"].id,
                        permission_id=permissions_by_name[perm_name].id
                    )
                )

        for perm_name in admin_perms:
            if perm_name in permissions_by_name:
                await db.execute(
                    insert(RolePermission).values(
                        role_id=roles["admin"].id,
                        permission_id=permissions_by_name[perm_name].id
                    )
                )

        for perm_name in super_admin_perms:
            if perm_name in permissions_by_name:
                await db.execute(
                    insert(RolePermission).values(
                        role_id=roles["super_admin"].id,
                        permission_id=permissions_by_name[perm_name].id
                    )
                )

        await db.commit()
        print("Assigned permissions to roles")


async def seed_default_tenant():
    """Seed default tenant."""
    async with AsyncSessionLocal() as db:
        # Check if tenant already exists
        result = await db.execute(
            select(Tenant).where(Tenant.company_name == "Default Organization")
        )
        existing_tenant = result.scalar_one_or_none()

        if existing_tenant:
            print("Default tenant already exists, skipping...")
            return

        # Create default tenant
        tenant = Tenant(
            company_name="Default Organization",
            plan="free",
            is_active=True
        )
        db.add(tenant)
        await db.commit()
        print("Created default tenant")


async def seed_admin_user():
    """Seed default admin user for testing."""
    async with AsyncSessionLocal() as db:
        # Check if admin user already exists
        result = await db.execute(
            select(User).where(User.email == "admin@valargen.com")
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            print("Admin user already exists, skipping...")
            return

        # Get tenant and role
        result = await db.execute(
            select(Tenant).where(Tenant.company_name == "Default Organization")
        )
        tenant = result.scalar_one_or_none()

        result = await db.execute(select(Role).where(Role.name == "admin"))
        admin_role = result.scalar_one_or_none()

        if not tenant or not admin_role:
            print("Error: Tenant or admin role not found. Run seed_roles and seed_default_tenant first.")
            return

        # Create admin user
        user = User(
            email="admin@valargen.com",
            password_hash=password_service.hash_password("Admin123"),
            first_name="Admin",
            last_name="User",
            auth_provider="local",
            is_email_verified=True,
            tenant_id=tenant.id,
            role_id=admin_role.id
        )
        db.add(user)
        await db.commit()

        print("\n" + "="*80)
        print("DEFAULT ADMIN USER CREATED")
        print("="*80)
        print("Email: admin@valargen.com")
        print("Password: Admin123")
        print("="*80 + "\n")


async def main():
    """Run all seed functions."""
    print("Starting database seeding...\n")

    try:
        await seed_roles()
        await seed_permissions()
        await assign_role_permissions()
        await seed_default_tenant()
        await seed_admin_user()

        print("\nDatabase seeding completed successfully!")

    except Exception as e:
        print(f"\nError during seeding: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
