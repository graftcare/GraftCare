import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from supabase_client import supabase

print("\n" + "="*70)
print("POPULATING TEST DATA")
print("="*70 + "\n")

# Create vendor
print("1. Creating test vendor...")
vendor_data = {
    "name": "Test Pharma Supplier",
    "contact_person": "John Doe",
    "phone": "+91-9876543210",
    "gstin": "27AABCP1234R1Z0",
    "city": "Mumbai",
    "address": "123 Main Street"
}

try:
    response = supabase.table("vendors").insert([vendor_data]).execute()
    if response.data:
        vendor_id = response.data[0]["id"]
        print(f"   [OK] Vendor created: {vendor_id}")
    else:
        print("   [ERR] Failed to create vendor")
        vendor_id = None
except Exception as e:
    print(f"   [ERR] {str(e)[:80]}")
    vendor_id = None

# Create product
print("\n2. Creating test product...")
product_data = {
    "name": "Paracetamol 500mg",
    "hsn_code": "3004",
    "company": "Cipla",
    "cost_price": 5.00,
    "mrp": 10.00,
    "gst_rate": 5.0
}

try:
    response = supabase.table("products").insert([product_data]).execute()
    if response.data:
        product_id = response.data[0]["id"]
        print(f"   [OK] Product created: {product_id}")
    else:
        print("   [ERR] Failed to create product")
        product_id = None
except Exception as e:
    print(f"   [ERR] {str(e)[:80]}")
    product_id = None

print("\n" + "="*70 + "\n")
if vendor_id and product_id:
    print(f"Ready for testing!")
    print(f"Vendor ID: {vendor_id}")
    print(f"Product ID: {product_id}")
else:
    print("Failed to create test data")
