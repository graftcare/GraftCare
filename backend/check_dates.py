import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from supabase_client import supabase

print("\n" + "="*70)
print("CHECKING DATE FORMATS IN DATABASE")
print("="*70 + "\n")

# Check purchase invoices
print("1. PURCHASE INVOICES - Invoice Dates:")
print("-" * 70)
try:
    response = supabase.table("purchase_invoices").select("id, vendor_invoice_no, invoice_date").execute()
    invoices = response.data if response.data else []
    
    if invoices:
        for inv in invoices:
            print(f"Invoice: {inv['vendor_invoice_no']}")
            print(f"  Date: {inv['invoice_date']}")
            print(f"  Date Type: {type(inv['invoice_date']).__name__}")
            print()
    else:
        print("No invoices found\n")
except Exception as e:
    print(f"Error: {str(e)[:80]}\n")

# Check purchase items with expiry
print("2. PURCHASE ITEMS - Expiry Dates:")
print("-" * 70)
try:
    response = supabase.table("purchase_items").select("id, product_id, batch, expiry, qty").execute()
    items = response.data if response.data else []
    
    if items:
        for item in items:
            print(f"Batch: {item['batch']}")
            print(f"  Expiry: {item['expiry']}")
            print(f"  Expiry Type: {type(item['expiry']).__name__}")
            print(f"  Qty: {item['qty']}")
            print()
    else:
        print("No items found\n")
except Exception as e:
    print(f"Error: {str(e)[:80]}\n")

# Check sales items
print("3. SALES ITEMS - Expiry Dates:")
print("-" * 70)
try:
    response = supabase.table("sales_items").select("id, product_id, batch, expiry, qty").execute()
    items = response.data if response.data else []
    
    if items:
        for item in items:
            print(f"Batch: {item['batch']}")
            print(f"  Expiry: {item['expiry']}")
            print(f"  Expiry Type: {type(item['expiry']).__name__}")
            print(f"  Qty: {item['qty']}")
            print()
    else:
        print("No items found\n")
except Exception as e:
    print(f"Error: {str(e)[:80]}\n")

print("="*70 + "\n")
