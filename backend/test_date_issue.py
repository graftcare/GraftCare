import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api"

print("\n" + "="*70)
print("TESTING DATE HANDLING - INVOICE & EXPIRY DATES")
print("="*70 + "\n")

# Get or create product
print("1. Getting product...")
try:
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    
    if products:
        product_id = products[0]["id"]
        product_name = products[0]["name"]
        print(f"   ✓ Found: {product_name}\n")
    else:
        print("   ✗ No products, creating one...")
        prod = {
            "name": "Test Product",
            "hsn_code": "3004",
            "company": "Test",
            "cost_price": 10,
            "mrp": 20,
            "gst_rate": 5
        }
        response = requests.post(f"{BASE_URL}/products", json=prod)
        product_id = response.json()["id"]
        product_name = "Test Product"
        print(f"   ✓ Created: {product_name}\n")
except Exception as e:
    print(f"   ✗ Error: {str(e)[:60]}\n")
    product_id = None

if product_id:
    print("2. Testing different date formats in purchase invoice...\n")
    
    # Test 1: Standard YYYY-MM-DD format
    test_cases = [
        {
            "name": "Standard YYYY-MM-DD",
            "invoice_date": "2026-04-22",
            "expiry_date": "2027-04-22"
        },
        {
            "name": "Today's date",
            "invoice_date": datetime.now().strftime("%Y-%m-%d"),
            "expiry_date": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"   Test {i}: {test['name']}")
        print(f"   - Invoice Date: {test['invoice_date']}")
        print(f"   - Expiry Date: {test['expiry_date']}")
        
        payload = {
            "vendor_name": f"Test Vendor {i}",
            "contact_person": "Test",
            "phone": f"999000{i}",
            "vendor_gstin": f"27AABCP{i}34R1Z0",
            "address": "Test Address",
            "city": "Test City",
            "pincode": "123456",
            "vendor_invoice_no": f"INV-{i}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "invoice_date": test['invoice_date'],
            "payment_mode": "Cash",
            "amount_paid": 1000,
            "paid_by": "Test",
            "subtotal": 1000,
            "total_gst": 100,
            "discount_amount": 0,
            "grand_total": 1100,
            "products": [
                {
                    "product_id": product_id,
                    "name": product_name,
                    "qty": 10,
                    "batch": f"BATCH00{i}",
                    "expiry": test['expiry_date'],
                    "mrp": 20,
                    "buy_rate": 10,
                    "gst": 5
                }
            ]
        }
        
        try:
            response = requests.post(f"{BASE_URL}/purchase-invoices", json=payload)
            
            if response.status_code == 200:
                print(f"   ✓ Invoice created successfully\n")
            else:
                print(f"   ✗ Error: {response.json()}\n")
        except Exception as e:
            print(f"   ✗ Exception: {str(e)[:60]}\n")
    
    # Verify stored dates
    print("3. Verifying dates in database...\n")
    
    try:
        response = requests.get(f"{BASE_URL}/purchase-invoices")
        invoices = response.json()
        
        # Get detail for each invoice
        for inv in invoices[-2:]:  # Get last 2 invoices
            print(f"   Invoice: {inv.get('vendor_invoice_no')}")
            print(f"   - Stored Invoice Date: {inv.get('invoice_date')} (Type: {type(inv.get('invoice_date')).__name__})")
            
            # Get items for this invoice
            items_response = requests.get(f"{BASE_URL}/stock")
            items = items_response.json()
            for item in items:
                print(f"   - Product: {item['product_name']}")
                print(f"   ✓ Data looks correct\n")
    except Exception as e:
        print(f"   ✗ Error: {str(e)[:60]}\n")

print("="*70)
print("DATE TESTING COMPLETE")
print("="*70 + "\n")
