import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api"

print("\n" + "="*70)
print("TESTING PURCHASE INVOICE WITH AUTO VENDOR CREATION")
print("="*70 + "\n")

# Get a product first
print("1. Getting products...")
try:
    response = requests.get(f"{BASE_URL}/products")
    products = response.json() if response.status_code == 200 else []
    
    if not products:
        print("   [ERR] No products found, creating test product...")
        prod_data = {
            "name": "Ibuprofen 200mg",
            "hsn_code": "3004",
            "company": "Mankind",
            "cost_price": 8.00,
            "mrp": 15.00,
            "gst_rate": 5.0
        }
        response = requests.post(f"{BASE_URL}/products", json=prod_data)
        if response.status_code == 200:
            product_id = response.json()["id"]
            print(f"   [OK] Product created: {product_id}")
        else:
            print(f"   [ERR] {response.json()}")
            product_id = None
    else:
        product_id = products[0]["id"]
        print(f"   [OK] Found product: {products[0]['name']}")
except Exception as e:
    print(f"   [ERR] {str(e)[:80]}")
    product_id = None

if product_id:
    print("\n2. Creating purchase invoice with NEW vendor...")
    
    # This vendor doesn't exist yet - it should be auto-created
    purchase_invoice = {
        "vendor_name": "Madhura Distributor",
        "contact_person": "Bhagwan",
        "phone": "0939024243",
        "vendor_gstin": "897238RNK2L3982",
        "dl_no_1": "729/728/626793",
        "dl_no_2": "729/728/626793",
        "address": "aramghar",
        "city": "hyderabad",
        "pincode": "500053",
        "vendor_bank_name": "sdhwrh44v",
        "vendor_account_no": "4trvgresfhfs",
        "vendor_ifsc": "",
        "vendor_invoice_no": f"PO-2026-{int(datetime.now().timestamp()) % 10000}",
        "invoice_date": datetime.now().strftime("%Y-%m-%d"),
        "payment_mode": "Cash",
        "amount_paid": 62885,
        "paid_by": "Bhagwan",
        "subtotal": 42500,
        "total_gst": 2125,
        "discount_amount": 0,
        "grand_total": 44625,
        "note": "353gred",
        "products": [
            {
                "product_id": product_id,
                "qty": 100,
                "batch": "BATCH2024001",
                "expiry": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
                "mrp": 15,
                "buy_rate": 8,
                "free": 0,
                "discount": 0,
                "gst": 5
            }
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/purchase-invoices", json=purchase_invoice)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   [OK] Invoice created: {result.get('id')}")
            print(f"   [OK] {result.get('message')}")
        else:
            print(f"   [ERR] {response.json()}")
    except Exception as e:
        print(f"   [ERR] {str(e)[:100]}")

print("\n" + "="*70 + "\n")
