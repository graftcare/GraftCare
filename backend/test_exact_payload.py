import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api"

print("\n" + "="*70)
print("TESTING EXACT PAYLOAD FROM UI")
print("="*70 + "\n")

# First get a product ID to use in the payload
print("1. Getting product ID...")
try:
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    
    if products:
        product_id = products[0]["id"]
        product_name = products[0]["name"]
        print(f"   [OK] Found product: {product_name} ({product_id[:8]}...)\n")
    else:
        print("   [ERR] No products found")
        product_id = None
except Exception as e:
    print(f"   [ERR] {str(e)[:80]}")
    product_id = None

if product_id:
    print("2. Creating purchase invoice with exact payload structure...\n")
    
    # Exact payload structure from the user
    payload = {
        "vendor_name": "Madhura Distributors",
        "contact_person": "The AI Shastra",
        "address": "aramghar",
        "amount_paid": 65000,
        "city": "hyderabad",
        "discount_amount": 238.095,
        "dl_no_1": "729/728/626793",
        "dl_no_2": "",
        "grand_total": 5011.905,
        "invoice_date": "2026-04-22",
        "note": "353gred",
        "paid_by": "Bhagwan",
        "payment_mode": "Cash",
        "phone": "0939024243",
        "pincode": "500053",
        "subtotal": 5000,
        "total_gst": 250,
        "vendor_account_no": "4trvgresfhfs",
        "vendor_bank_name": "sdhwrh44v",
        "vendor_gstin": "897238RNK2L3982",
        "vendor_ifsc": "5435btte",
        "vendor_invoice_no": "PO-2026-54866",
        "products": [
            {
                "product_id": product_id,
                "name": product_name,
                "qty": 100,
                "batch": "BATCH2024001",
                "expiry": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
                "mrp": 50,
                "buy_rate": 25,
                "free": 0,
                "discount": 0,
                "gst": 5
            }
        ]
    }
    
    try:
        print(f"   Payload:")
        print(f"   - Vendor: {payload['vendor_name']}")
        print(f"   - Invoice #: {payload['vendor_invoice_no']}")
        print(f"   - Date: {payload['invoice_date']}")
        print(f"   - Amount: ₹{payload['grand_total']}")
        print(f"   - Products: {len(payload['products'])} item(s)")
        print(f"   - Product: {product_name} x {payload['products'][0]['qty']}")
        print()
        
        response = requests.post(f"{BASE_URL}/purchase-invoices", json=payload)
        print(f"   Status: {response.status_code}\n")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   [OK] SUCCESS!")
            print(f"   [OK] Invoice ID: {result.get('id')}")
            print(f"   [OK] Message: {result.get('message')}")
        else:
            error = response.json()
            print(f"   [ERR] Error: {error}")
    except Exception as e:
        print(f"   [ERR] Exception: {str(e)[:100]}")

print("\n" + "="*70)
print("VERIFYING DATA WAS SAVED")
print("="*70 + "\n")

# Verify the data
try:
    print("1. Checking vendors...")
    response = requests.get(f"{BASE_URL}/vendors")
    vendors = response.json()
    madhura = next((v for v in vendors if "Madhura" in v.get("name", "")), None)
    if madhura:
        print(f"   [OK] Vendor found: {madhura['name']}")
    
    print("\n2. Checking stock...")
    response = requests.get(f"{BASE_URL}/stock")
    stocks = response.json()
    for stock in stocks:
        print(f"   [OK] {stock['product_name']}")
        print(f"       Purchased: {stock['purchased']}, Sold: {stock['sold']}, Available: {stock['available']}")
    
    print("\n3. Checking dashboard...")
    response = requests.get(f"{BASE_URL}/dashboard")
    data = response.json()
    print(f"   [OK] Total Stock: {data.get('total_stock', 0)} units")
    print(f"   [OK] Total Invoices: {data.get('total_invoices', 0)}")
    print(f"   [OK] Total Purchases: ₹{data.get('total_purchases', 0):,.2f}")
    
except Exception as e:
    print(f"   [ERR] {str(e)[:80]}")

print("\n" + "="*70 + "\n")
