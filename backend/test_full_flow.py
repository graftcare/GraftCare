import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api"

print("\n" + "="*70)
print("COMPLETE FLOW TEST: CREATE PRODUCT → INVOICE → VERIFY STOCK")
print("="*70 + "\n")

# Step 1: Create a product
print("STEP 1: Creating product...")
product_data = {
    "name": "Dolo 650",
    "hsn_code": "3004",
    "company": "Micro Labs",
    "cost_price": 25,
    "mrp": 50,
    "gst_rate": 5
}

try:
    response = requests.post(f"{BASE_URL}/products", json=product_data)
    if response.status_code == 200:
        product_id = response.json()["id"]
        print(f"✓ Product created: {product_id[:8]}...")
    else:
        print(f"✗ Error: {response.json()}")
        product_id = None
except Exception as e:
    print(f"✗ Error: {str(e)[:60]}")
    product_id = None

if product_id:
    # Step 2: Create purchase invoice with exact payload structure
    print("\nSTEP 2: Creating purchase invoice with exact payload...")
    
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
                "name": "Dolo 650",
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
        response = requests.post(f"{BASE_URL}/purchase-invoices", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            invoice_id = result.get('id')
            print(f"✓ Invoice created: {invoice_id[:8]}...")
            print(f"✓ {result.get('message')}")
        else:
            print(f"✗ Error: {response.json()}")
            invoice_id = None
    except Exception as e:
        print(f"✗ Error: {str(e)[:60]}")
        invoice_id = None
    
    # Step 3: Verify stock updated
    if invoice_id:
        print("\nSTEP 3: Verifying stock was updated...")
        
        try:
            response = requests.get(f"{BASE_URL}/stock")
            stocks = response.json()
            
            if stocks:
                for stock in stocks:
                    print(f"✓ {stock['product_name']}")
                    print(f"  - Purchased: {stock['purchased']} units")
                    print(f"  - Sold: {stock['sold']} units")
                    print(f"  - Available: {stock['available']} units")
        except Exception as e:
            print(f"✗ Error: {str(e)[:60]}")
        
        # Step 4: Check dashboard
        print("\nSTEP 4: Checking dashboard...")
        
        try:
            response = requests.get(f"{BASE_URL}/dashboard")
            data = response.json()
            
            print(f"✓ Dashboard Summary:")
            print(f"  - Total Stock: {data.get('total_stock', 0)} units 📦")
            print(f"  - Total Products: {data.get('total_products', 0)}")
            print(f"  - Total Vendors: {data.get('total_vendors', 0)}")
            print(f"  - Total Purchases: ₹{data.get('total_purchases', 0):,.2f}")
            print(f"  - Total Invoices: {data.get('total_invoices', 0)}")
        except Exception as e:
            print(f"✗ Error: {str(e)[:60]}")

print("\n" + "="*70)
print("✓ COMPLETE FLOW TEST FINISHED")
print("="*70 + "\n")
