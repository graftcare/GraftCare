import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api"

print("\n" + "="*70)
print("TESTING PURCHASE INVOICE ENDPOINT")
print("="*70 + "\n")

# First, get a vendor
print("1. Getting vendors...")
try:
    response = requests.get(f"{BASE_URL}/vendors")
    if response.status_code == 200:
        vendors = response.json()
        if vendors:
            vendor = vendors[0]
            vendor_id = vendor["id"]
            vendor_name = vendor["name"]
            print(f"   [OK] Found vendor: {vendor_name}")
        else:
            print("   [ERR] No vendors found")
            vendor_id = None
    else:
        print(f"   [ERR] Error getting vendors: {response.status_code}")
        vendor_id = None
except Exception as e:
    print(f"   [ERR] {str(e)[:80]}")
    vendor_id = None

# Get products
print("\n2. Getting products...")
try:
    response = requests.get(f"{BASE_URL}/products")
    if response.status_code == 200:
        products = response.json()
        if products:
            product = products[0]
            product_id = product["id"]
            product_name = product["name"]
            print(f"   [OK] Found product: {product_name}")
        else:
            print("   [ERR] No products found")
            product_id = None
    else:
        print(f"   [ERR] Error getting products")
        product_id = None
except Exception as e:
    print(f"   [ERR] {str(e)[:80]}")
    product_id = None

# Create purchase invoice if we have vendor and product
if vendor_id and product_id:
    print("\n3. Creating purchase invoice...")
    
    purchase_invoice = {
        "vendor_id": vendor_id,
        "vendor_invoice_no": f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "invoice_date": datetime.now().strftime("%Y-%m-%d"),
        "payment_mode": "Bank Transfer",
        "amount_paid": 1000,
        "paid_by": "Cheque",
        "subtotal": 1000,
        "total_gst": 180,
        "discount_amount": 0,
        "grand_total": 1180,
        "payment_status": "pending",
        "items": [
            {
                "product_id": product_id,
                "qty": 50,
                "batch": "BATCH2024001",
                "expiry": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
                "mrp": 100,
                "buy_rate": 50,
                "free": 0,
                "discount": 0,
                "gst": 18
            }
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/purchase-invoices", json=purchase_invoice)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   [OK] Purchase invoice created: {result.get('id')}")
            print(f"   [OK] {result.get('message')}")
        else:
            print(f"   [ERR] Error: {response.json()}")
    except Exception as e:
        print(f"   [ERR] {str(e)[:80]}")
else:
    print("\n[ERR] Missing vendor or product, skipping invoice creation")

print("\n" + "="*70 + "\n")
