import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests

BASE_URL = "http://localhost:8000/api"

print("\n" + "="*70)
print("TESTING DASHBOARD ENDPOINT")
print("="*70 + "\n")

try:
    print("Calling /api/dashboard...")
    response = requests.get(f"{BASE_URL}/dashboard", timeout=5)
    
    print(f"Status Code: {response.status_code}\n")
    
    if response.status_code == 200:
        data = response.json()
        
        print("Dashboard Data:")
        print("-" * 70)
        print(f"  Total Products:     {data.get('total_products', 0)}")
        print(f"  Total Stock Units:  {data.get('total_stock', 0)} 📦")
        print(f"  Total Vendors:      {data.get('total_vendors', 0)}")
        print(f"  Total Purchases:    ₹{data.get('total_purchases', 0):,.2f}")
        print(f"  Total Sales:        ₹{data.get('total_sales', 0):,.2f}")
        print(f"  Expiring Soon:      {data.get('expiring_soon', 0)}")
        print(f"  Total Invoices:     {data.get('total_invoices', 0)}")
        print(f"  Total Sales Orders: {data.get('total_sales_orders', 0)}")
        print("-" * 70)
    else:
        print(f"[ERR] Error: {response.json()}")
        
except requests.exceptions.ConnectionError:
    print("[ERR] Cannot connect to server")
except Exception as e:
    print(f"[ERR] {str(e)[:100]}")

print("\n" + "="*70 + "\n")
