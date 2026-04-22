import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from supabase_client import supabase

print("\n" + "="*70)
print("VERIFYING DATES ARE PROPERLY STORED")
print("="*70 + "\n")

# Check all purchase invoices with their items
try:
    inv_response = supabase.table("purchase_invoices").select("id, vendor_invoice_no, invoice_date").execute()
    invoices = inv_response.data if inv_response.data else []
    
    print(f"Total Invoices: {len(invoices)}\n")
    
    for inv in invoices:
        print(f"Invoice: {inv['vendor_invoice_no']}")
        print(f"Invoice Date: {inv['invoice_date']}")
        
        # Get items for this invoice
        items_response = supabase.table("purchase_items").select("product_id, batch, expiry, qty").eq("purchase_invoice_id", inv['id']).execute()
        items = items_response.data if items_response.data else []
        
        if items:
            for item in items:
                print(f"  - Batch: {item['batch']}, Expiry: {item['expiry']}, Qty: {item['qty']}")
        else:
            print(f"  - No items")
        print()
        
except Exception as e:
    print(f"Error: {str(e)[:100]}")

print("="*70)
print("\n✓ If you see dates above (YYYY-MM-DD format), dates are stored correctly!")
print("  If you see NULL or empty dates, there's an issue to fix.\n")
