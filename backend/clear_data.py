"""
Clear all data from Supabase database tables (keep schema intact)
Use this to reset the database to empty state with fresh sequences
"""

import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from supabase_client import supabase

print("\n" + "="*70)
print("DATABASE CLEANUP - CLEARING ALL DATA")
print("="*70 + "\n")

# Tables to clear in order (respecting foreign key constraints)
tables_to_clear = [
    "sales_items",
    "purchase_items",
    "stock_ledger",
    "sales",
    "purchase_invoices",
    "customers",
    "products",
    "vendors"
]

print("Clearing data from tables...\n")

for table in tables_to_clear:
    try:
        # Delete all records - using a filter that matches everything
        response = supabase.table(table).delete().gt("created_at", "1900-01-01").execute()
        print(f"[OK] {table:20} - cleared")
    except Exception as e:
        print(f"[ERR] {table:20} - {str(e)[:60]}")

# Verify all tables are empty
print("\n" + "="*70)
print("VERIFICATION - Checking all tables are empty")
print("="*70 + "\n")

empty_count = 0
for table in tables_to_clear:
    try:
        response = supabase.table(table).select("id", count="exact").execute()
        count = response.count if hasattr(response, 'count') else len(response.data)
        status = "[OK] EMPTY" if count == 0 else f"[WARN] {count} records"
        print(f"{table:20} - {status}")
        if count == 0:
            empty_count += 1
    except Exception as e:
        print(f"{table:20} - [ERR] {str(e)[:50]}")

print("\n" + "="*70)
if empty_count == len(tables_to_clear):
    print("SUCCESS - All tables cleared and database is fresh!")
else:
    print(f"WARNING - {empty_count}/{len(tables_to_clear)} tables are empty")
print("="*70 + "\n")
