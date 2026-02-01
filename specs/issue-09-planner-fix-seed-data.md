# Plan: Fix Seed Data Script - RolePermission Table Issue

## Description
The `seed_data.py` script is failing with the error:
```
TypeError: 'Table' object is not callable
```

This occurs in the `assign_role_permissions()` function when trying to create RolePermission records. The issue is that `RolePermission` is defined as a SQLAlchemy `Table` object (association table for many-to-many relationship), not an ORM model class. The script incorrectly tries to instantiate it like a class: `RolePermission(role_id=..., permission_id=...)`.

The fix requires using SQLAlchemy's `insert()` statement to insert rows into the association table instead of instantiating it as a class.

## Relevant Files
Use these files to resolve the chore:

- `app/server/scripts/seed_data.py` - The main seed script with the bug in `assign_role_permissions()` function at lines 146-165. This is where `RolePermission()` is incorrectly called as a constructor.
- `app/server/models/permission.py` - Contains the `RolePermission` definition as a `Table` object (lines 16-21), confirming it's not an ORM model class.
- `app/server/scripts/seed_customers.py` - Reference for how other seed scripts work (this one works correctly).
- `app/server/database.py` - Database session management.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Fix the assign_role_permissions Function

- Modify `app/server/scripts/seed_data.py`:
  - Import the `insert` function from SQLAlchemy at the top of the file:
    ```python
    from sqlalchemy import select, insert
    ```
  - Replace the `db.add(RolePermission(...))` calls with proper `insert()` statements
  - The fix should change from:
    ```python
    db.add(RolePermission(
        role_id=roles["loan_officer"].id,
        permission_id=permissions_by_name[perm_name].id
    ))
    ```
  - To:
    ```python
    await db.execute(
        insert(RolePermission).values(
            role_id=roles["loan_officer"].id,
            permission_id=permissions_by_name[perm_name].id
        )
    )
    ```
  - Apply this fix to all three permission assignment blocks (loan_officer, admin, super_admin)

### Step 2: Test the Seed Script

- Run the seed_data.py script to verify the fix:
  ```bash
  cd app/server && uv run python scripts/seed_data.py
  ```
- Verify that role permissions are successfully assigned

### Step 3: Test the Customer Seed Script

- Run the seed_customers.py script to verify it still works:
  ```bash
  cd app/server && uv run python scripts/seed_customers.py
  ```

### Step 4: Run Validation Commands

- Run all validation commands to ensure the chore is complete with zero regressions

## Validation Commands
Execute every command to validate the chore is complete with zero regressions.

- `cd app/server && uv run python scripts/seed_data.py` - Run seed_data script to verify it completes without errors
- `cd app/server && uv run python scripts/seed_customers.py` - Run seed_customers script to verify customers are seeded
- `cd app/server && uv run pytest` - Run server tests to validate no regressions

## Notes

### Root Cause
The `RolePermission` is defined as a SQLAlchemy `Table` object for many-to-many relationships:
```python
RolePermission = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True),
)
```

`Table` objects cannot be instantiated like ORM model classes. Instead, you must use `insert()` to add rows to association tables.

### Alternative Approach
Another option would be to use the relationship directly:
```python
role.permissions.append(permission)
```
However, this requires loading the relationship which may cause async issues. The `insert()` approach is cleaner for seeding.

### Database State
If the database already has partial data from previous failed runs, you may need to:
1. Clear the `role_permissions` table first, or
2. Drop and recreate the database using migrations:
   ```bash
   cd app/server && alembic downgrade base && alembic upgrade head
   ```
