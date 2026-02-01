"""
Seed customer data for Valargen database.

Run with: uv run python scripts/seed_customers.py
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import select

from database import AsyncSessionLocal
from models.tenant import Tenant
from models.customer import Customer


async def seed_customers():
    """Seed 15 sample customer records for each tenant."""
    async with AsyncSessionLocal() as db:
        # Get all tenants
        result = await db.execute(select(Tenant))
        tenants = result.scalars().all()

        if not tenants:
            print("No tenants found. Please run seed_data.py first.")
            return

        # Sample customer data
        sample_customers = [
            {
                "name": "John Smith",
                "email": "john.smith@example.com",
                "phone": "(555) 123-4567",
                "company_name": "Smith Construction LLC"
            },
            {
                "name": "Emily Johnson",
                "email": "emily.johnson@example.com",
                "phone": "(555) 234-5678",
                "company_name": "Johnson Real Estate"
            },
            {
                "name": "Michael Brown",
                "email": "michael.brown@example.com",
                "phone": "(555) 345-6789",
                "company_name": "Brown & Associates"
            },
            {
                "name": "Sarah Davis",
                "email": "sarah.davis@example.com",
                "phone": "(555) 456-7890",
                "company_name": None
            },
            {
                "name": "David Wilson",
                "email": "david.wilson@example.com",
                "phone": "(555) 567-8901",
                "company_name": "Wilson Properties"
            },
            {
                "name": "Jessica Martinez",
                "email": "jessica.martinez@example.com",
                "phone": "(555) 678-9012",
                "company_name": "Martinez Holdings"
            },
            {
                "name": "Robert Taylor",
                "email": "robert.taylor@example.com",
                "phone": "(555) 789-0123",
                "company_name": "Taylor Development Group"
            },
            {
                "name": "Linda Anderson",
                "email": "linda.anderson@example.com",
                "phone": "(555) 890-1234",
                "company_name": None
            },
            {
                "name": "James Thomas",
                "email": "james.thomas@example.com",
                "phone": "(555) 901-2345",
                "company_name": "Thomas Investments"
            },
            {
                "name": "Patricia Jackson",
                "email": "patricia.jackson@example.com",
                "phone": "(555) 012-3456",
                "company_name": "Jackson Realty Partners"
            },
            {
                "name": "Christopher White",
                "email": "christopher.white@example.com",
                "phone": "(555) 123-4568",
                "company_name": "White Capital Management"
            },
            {
                "name": "Jennifer Harris",
                "email": "jennifer.harris@example.com",
                "phone": "(555) 234-5679",
                "company_name": None
            },
            {
                "name": "Daniel Martin",
                "email": "daniel.martin@example.com",
                "phone": "(555) 345-6780",
                "company_name": "Martin Enterprises"
            },
            {
                "name": "Nancy Thompson",
                "email": "nancy.thompson@example.com",
                "phone": "(555) 456-7891",
                "company_name": "Thompson Financial Services"
            },
            {
                "name": "Matthew Garcia",
                "email": "matthew.garcia@example.com",
                "phone": "(555) 567-8902",
                "company_name": "Garcia Property Group"
            }
        ]

        total_created = 0

        for tenant in tenants:
            # Check if customers already exist for this tenant
            result = await db.execute(
                select(Customer).where(Customer.tenant_id == tenant.id)
            )
            existing_customers = result.scalars().all()

            if existing_customers:
                print(f"Customers already exist for tenant '{tenant.company_name}', skipping...")
                continue

            # Create customers for this tenant
            for customer_data in sample_customers:
                customer = Customer(
                    name=customer_data["name"],
                    email=customer_data["email"],
                    phone=customer_data["phone"],
                    company_name=customer_data["company_name"],
                    tenant_id=tenant.id
                )
                db.add(customer)
                total_created += 1

            await db.commit()
            print(f"Created {len(sample_customers)} customers for tenant '{tenant.company_name}'")

        if total_created > 0:
            print(f"\nTotal customers created: {total_created}")
        else:
            print("\nNo new customers created (all tenants already have customers)")


async def main():
    """Run customer seeding."""
    print("Starting customer seeding...\n")

    try:
        await seed_customers()
        print("\nCustomer seeding completed successfully!")

    except Exception as e:
        print(f"\nError during seeding: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
