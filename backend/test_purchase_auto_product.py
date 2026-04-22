import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api"

print("\n" + "="*70)
print("TESTING PURCHASE WITH AUTO PRODUCT CREATION")
print("="*70 + "\n")

print("Creating purchase invoice with NEW product 'Dolo 650'...\n")

purchase_invoice = {
    "vendor_name": "Madhura Distributors",
    "contact_person": "The AI Shastra",
    "phone": "0939024243",
    "vendor_gstin": "897238RNK2L3982",
    "dl_no_1": "729/728/626793",
    "dl_no_2": "",
    "address": "aramghar",
    "city": "hyderabad",
    "pincode": "500053",
    "vendor_bank_name": "sdhwrh44v",
    "vendor_account_no": "4trvgresfhfs",
    "vendor_ifsc": "5435btte",
    "vendor_invoice_no": f"PO-2026-{int(datetime.now().timestamp()) % 10000}",
    "invoice_date": datetime.now().strftime("%Y-%m-%d"),
    "payment_mode": "Cash",
    "amount_paid": 65000,
    "paid_by": "Bhagwan",
    "subtotal": 5000,
    "total_gst": 250,
    "discount_amount": 238.095,
    "grand_total": 5011.905,
    "note": "353gred",
    "products": [
        {
            "name": "Dolo 650",  # This product doesn't exist yet
            "qty": 100,
            "batch": "BATCH2024001",
            "expiry": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
            "mrp": 50,
            "buy_rate": 25,
            "free": 0,
            "discount": 0,
            "gst": 5,
            "company": "Micro Labs",
            "hsn_code": "3004"
        }
    ]
}

try:
    response = requests.post(f"{BASE_URL}/purchase-invoices", json=purchase_invoice)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"[OK] Invoice created: {result.get('id')}")
        print(f"[OK] {result.get('message')}")
    else:
        print(f"[ERR] Error: {response.json()}")
except Exception as e:
    print(f"[ERR] {str(e)[:100]}")

print("\n" + "="*70)
print("Verifying products were created...")
print("="*70 + "\n")

try:
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    
    print(f"Total products: {len(products)}\n")
    for p in products:
        print(f"- {p['name']:30} (ID: {p['id'][:8]}...)")
        print(f"  HSN: {p.get('hsn_code')}, Cost: {p.get('cost_price')}, MRP: {p.get('mrp')}\n")
except Exception as e:
    print(f"Error: {str(e)[:80]}")

print("="*70 + "\n")
