import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from supabase_client import supabase

print("\n" + "="*70)
print("VERIFYING PRODUCTS ARE STORED CORRECTLY")
print("="*70 + "\n")

# Check products table
print("1. PRODUCTS TABLE:")
print("-" * 70)
try:
    response = supabase.table("products").select("id, name, cost_price, mrp").execute()
    products = response.data if response.data else []
    
    print(f"Total products: {len(products)}\n")
    
    for p in products:
        product_id = p['id']
        is_uuid = len(product_id) == 36 and product_id.count('-') == 4
        print(f"Product: {p['name']}")
        print(f"  ID: {product_id}")
        print(f"  Is UUID: {'YES ✓' if is_uuid else 'NO ✗'}")
        print(f"  Cost-MRP: {p['cost_price']}-{p['mrp']}\n")
except Exception as e:
    print(f"Error: {str(e)[:100]}")

# Check purchase_items table
print("\n2. PURCHASE_ITEMS TABLE:")
print("-" * 70)
try:
    response = supabase.table("purchase_items").select("product_id, qty, batch").execute()
    items = response.data if response.data else []
    
    print(f"Total purchase items: {len(items)}\n")
    
    for i, item in enumerate(items, 1):
        product_id = item['product_id']
        is_uuid = len(str(product_id)) == 36 and str(product_id).count('-') == 4
        print(f"{i}. Product ID: {product_id}")
        print(f"   Is UUID: {'YES ✓' if is_uuid else 'NO ✗'}")
        print(f"   Qty: {item['qty']}, Batch: {item.get('batch', 'N/A')}\n")
except Exception as e:
    print(f"Error: {str(e)[:100]}")

# Check stock_ledger table
print("\n3. STOCK_LEDGER TABLE:")
print("-" * 70)
try:
    response = supabase.table("stock_ledger").select("product_id, change_qty, reason").execute()
    ledger = response.data if response.data else []
    
    print(f"Total ledger entries: {len(ledger)}\n")
    
    for i, entry in enumerate(ledger, 1):
        product_id = entry['product_id']
        is_uuid = len(str(product_id)) == 36 and str(product_id).count('-') == 4
        print(f"{i}. Product ID: {product_id}")
        print(f"   Is UUID: {'YES ✓' if is_uuid else 'NO ✗'}")
        print(f"   Change: {entry['change_qty']}, Reason: {entry['reason']}\n")
except Exception as e:
    print(f"Error: {str(e)[:100]}")

print("="*70 + "\n")
