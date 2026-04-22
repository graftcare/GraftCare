"""
Test script for Supabase API endpoints
Run this after starting the FastAPI server: python main.py
"""

import requests
import json
import uuid
from datetime import datetime, timedelta
import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_URL = "http://localhost:8000/api"

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def test_vendors():
    """Test vendor endpoints"""
    print(f"\n{YELLOW}{'='*60}")
    print("TESTING: VENDORS")
    print(f"{'='*60}{RESET}\n")

    vendor_data = {
        "name": "Parag Pharmaceuticals",
        "contact_person": "John Doe",
        "phone": "+91-9876543210",
        "gstin": "27AABCP1234R1Z0",
        "dl1": "DL-001",
        "dl2": "DL-002",
        "address": "123 Main Street",
        "city": "Mumbai",
        "pincode": "400001",
        "bank_name": "HDFC Bank",
        "bank_acc": "1234567890",
        "bank_ifsc": "HDFC0000001"
    }

    # Create vendor
    print("1. Creating vendor...")
    response = requests.post(f"{BASE_URL}/vendors", json=vendor_data)
    if response.status_code == 200:
        vendor_id = response.json()["id"]
        print(f"{GREEN}✓ Vendor created: {vendor_id}{RESET}")
        return vendor_id
    else:
        print(f"{RED}✗ Error: {response.json()}{RESET}")
        return None

def test_products():
    """Test product endpoints"""
    print(f"\n{YELLOW}{'='*60}")
    print("TESTING: PRODUCTS")
    print(f"{'='*60}{RESET}\n")

    products = [
        {
            "name": "Paracetamol 500mg",
            "hsn_code": "3004",
            "pack": "10 tablets",
            "company": "Cipla",
            "scheme": "Scheme 1",
            "cost_price": 5.00,
            "mrp": 10.00,
            "gst_rate": 5.0
        },
        {
            "name": "Ibuprofen 200mg",
            "hsn_code": "3004",
            "pack": "20 tablets",
            "company": "Mankind",
            "scheme": "Scheme 2",
            "cost_price": 8.00,
            "mrp": 15.00,
            "gst_rate": 5.0
        }
    ]

    product_ids = []
    for i, product in enumerate(products, 1):
        print(f"{i}. Creating product: {product['name']}...")
        response = requests.post(f"{BASE_URL}/products", json=product)
        if response.status_code == 200:
            product_id = response.json()["id"]
            product_ids.append(product_id)
            print(f"{GREEN}✓ Product created: {product_id}{RESET}")
        else:
            print(f"{RED}✗ Error: {response.json()}{RESET}")

    return product_ids

def test_customers():
    """Test customer endpoints"""
    print(f"\n{YELLOW}{'='*60}")
    print("TESTING: CUSTOMERS")
    print(f"{'='*60}{RESET}\n")

    customer_data = {
        "name": "ABC Hospital",
        "contact_person": "Dr. Smith",
        "phone": "+91-8765432109",
        "gstin": "27AABCU9603R1Z0",
        "address": "456 Hospital Road",
        "city": "Delhi",
        "pincode": "110001",
        "credit_limit": 100000.00,
        "outstanding_balance": 0.00
    }

    print("1. Creating customer...")
    response = requests.post(f"{BASE_URL}/customers", json=customer_data)
    if response.status_code == 200:
        customer_id = response.json()["id"]
        print(f"{GREEN}✓ Customer created: {customer_id}{RESET}")
        return customer_id
    else:
        print(f"{RED}✗ Error: {response.json()}{RESET}")
        return None

def test_get_all():
    """Get all records"""
    print(f"\n{YELLOW}{'='*60}")
    print("TESTING: GET ALL RECORDS")
    print(f"{'='*60}{RESET}\n")

    endpoints = [
        ("vendors", "Vendors"),
        ("products", "Products"),
        ("customers", "Customers")
    ]

    for endpoint, name in endpoints:
        print(f"Getting all {name}...")
        response = requests.get(f"{BASE_URL}/{endpoint}")
        if response.status_code == 200:
            count = len(response.json())
            print(f"{GREEN}✓ Retrieved {count} {name}{RESET}")
            if count > 0:
                print(f"  Sample: {json.dumps(response.json()[0], indent=2, default=str)[:200]}...")
        else:
            print(f"{RED}✗ Error: {response.json()}{RESET}")

def test_purchase_invoice(vendor_id, product_ids):
    """Test purchase invoice endpoints"""
    print(f"\n{YELLOW}{'='*60}")
    print("TESTING: PURCHASE INVOICES")
    print(f"{'='*60}{RESET}\n")

    if not vendor_id or not product_ids:
        print(f"{RED}✗ Missing vendor or products. Skipping...{RESET}")
        return

    invoice_data = {
        "vendor_id": vendor_id,
        "vendor_invoice_no": f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "invoice_date": datetime.now().strftime("%Y-%m-%d"),
        "payment_mode": "Bank Transfer",
        "amount_paid": 500.00,
        "paid_by": "Cheque",
        "subtotal": 480.00,
        "total_gst": 20.00,
        "discount_amount": 0.00,
        "grand_total": 500.00,
        "payment_status": "pending",
        "items": [
            {
                "product_id": product_ids[0],
                "qty": 100,
                "batch": "BATCH2024001",
                "expiry": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
                "mrp": 10.00,
                "buy_rate": 5.00,
                "free": 0,
                "discount": 0.00,
                "gst": 5.0
            }
        ]
    }

    print("1. Creating purchase invoice...")
    response = requests.post(f"{BASE_URL}/purchase-invoices", json=invoice_data)
    if response.status_code == 200:
        invoice_id = response.json()["id"]
        print(f"{GREEN}✓ Purchase invoice created: {invoice_id}{RESET}")
        print(f"  Message: {response.json()['message']}")
        return invoice_id
    else:
        print(f"{RED}✗ Error: {response.json()}{RESET}")
        return None

def test_sales(customer_id, product_ids):
    """Test sales endpoints"""
    print(f"\n{YELLOW}{'='*60}")
    print("TESTING: SALES")
    print(f"{'='*60}{RESET}\n")

    if not customer_id or not product_ids:
        print(f"{RED}✗ Missing customer or products. Skipping...{RESET}")
        return

    sale_data = {
        "customer_id": customer_id,
        "status": "draft",
        "invoice_date": datetime.now().strftime("%Y-%m-%d"),
        "subtotal": 1500.00,
        "total_gst": 75.00,
        "discount_amount": 0.00,
        "grand_total": 1575.00,
        "payment_mode": "Cash",
        "amount_received": 1575.00,
        "items": [
            {
                "product_id": product_ids[0],
                "batch": "BATCH2024001",
                "expiry": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
                "qty": 10,
                "mrp": 10.00,
                "sale_rate": 9.00,
                "discount": 0.00,
                "gst": 5.0
            }
        ]
    }

    print("1. Creating sale...")
    response = requests.post(f"{BASE_URL}/sales", json=sale_data)
    if response.status_code == 200:
        sale_id = response.json()["id"]
        print(f"{GREEN}✓ Sale created: {sale_id}{RESET}")
        print(f"  Invoice Number: {response.json().get('invoice_number', 'N/A')}")
        return sale_id
    else:
        print(f"{RED}✗ Error: {response.json()}{RESET}")
        return None

def test_stock(product_ids):
    """Test stock endpoints"""
    print(f"\n{YELLOW}{'='*60}")
    print("TESTING: STOCK")
    print(f"{'='*60}{RESET}\n")

    if not product_ids:
        print(f"{RED}✗ No products. Skipping...{RESET}")
        return

    print("1. Getting all stock...")
    response = requests.get(f"{BASE_URL}/stock")
    if response.status_code == 200:
        stock = response.json()
        print(f"{GREEN}✓ Retrieved stock data{RESET}")
        for item in stock:
            print(f"  {item['product_name']}: {item['available']} units")
    else:
        print(f"{RED}✗ Error: {response.json()}{RESET}")

def main():
    """Run all tests"""
    print(f"\n{GREEN}{'='*60}")
    print("SUPABASE API TEST SUITE")
    print(f"{'='*60}{RESET}")
    print(f"Base URL: {BASE_URL}\n")

    try:
        # Test flow
        vendor_id = test_vendors()
        product_ids = test_products()
        customer_id = test_customers()
        test_get_all()

        if vendor_id and product_ids:
            test_purchase_invoice(vendor_id, product_ids)

        if customer_id and product_ids:
            test_sales(customer_id, product_ids)

        if product_ids:
            test_stock(product_ids)

        print(f"\n{GREEN}{'='*60}")
        print("✓ ALL TESTS COMPLETED")
        print(f"{'='*60}{RESET}\n")

    except requests.exceptions.ConnectionError:
        print(f"\n{RED}✗ ERROR: Cannot connect to API at {BASE_URL}")
        print("Make sure the FastAPI server is running:")
        print("  python main.py{RESET}\n")
    except Exception as e:
        print(f"\n{RED}✗ ERROR: {str(e)}{RESET}\n")

if __name__ == "__main__":
    main()
