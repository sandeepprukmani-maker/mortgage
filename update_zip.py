#!/usr/bin/env python3
"""
Script to update property_zip to 23266 for all customers in the database.
Run from the project root: python -m update_zip
"""

import sqlite3
import os

# Connect to the database
db_path = os.path.join(os.path.dirname(__file__), "instance", "project.db")

if not os.path.exists(db_path):
    print(f"Error: Database not found at {db_path}")
    exit(1)

print(f"Connecting to database at: {db_path}")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # First, check how many customers we have
    cursor.execute("SELECT COUNT(*) FROM customer")
    count = cursor.fetchone()[0]
    print(f"Found {count} customers in the database")

    # Update all customers' property_zip to 23219
    cursor.execute("UPDATE customer SET property_zip = '23219'")
    conn.commit()

    print(f"Successfully updated all {count} customers' property_zip to 23219")

    # Verify the update
    cursor.execute("SELECT id, name, property_zip FROM customer LIMIT 5")
    results = cursor.fetchall()
    print(f"\nVerification - showing first 5 customers:")
    for row in results:
        print(f"  Customer ID {row[0]}: {row[1]} - property_zip: {row[2]}")

except Exception as e:
    print(f"Error: {e}")
    conn.rollback()
finally:
    conn.close()
    print("\nDatabase connection closed.")

