import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from supabase_client import supabase

print("\n" + "="*60)
print("VERIFYING SUPABASE SCHEMA")
print("="*60 + "\n")

tables_to_check = [
    "vendors", "products", "customers", 
    "purchase_invoices", "purchase_items",
    "sales", "sales_items", "stock_ledger"
]

for table in tables_to_check:
    try:
        response = supabase.table(table).select("id", count="exact").execute()
        count = response.count if hasattr(response, 'count') else len(response.data)
        print(f"[OK] {table:20} - {count} records")
    except Exception as e:
        error_msg = str(e)[:50]
        print(f"[ERR] {table:20} - {error_msg}")

print("\n" + "="*60)
print("SCHEMA VERIFICATION COMPLETE")
print("="*60 + "\n")
