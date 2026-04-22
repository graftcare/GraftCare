import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests

BASE_URL = "http://localhost:8000/api"

print("\n" + "="*70)
print("TESTING UPDATED STOCK ENDPOINT")
print("="*70 + "\n")

try:
    print("Calling /api/stock...")
    response = requests.get(f"{BASE_URL}/stock", timeout=5)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        stocks = response.json()
        print(f"\nTotal products: {len(stocks)}\n")
        
        if stocks:
            print("Stock details with Purchased/Sold breakdown:")
            print("-" * 90)
            for stock in stocks:
                print(f"\nProduct: {stock['product_name']}")
                print(f"  Purchased: {stock.get('purchased', 0)}")
                print(f"  Sold:      {stock.get('sold', 0)}")
                print(f"  Available: {stock.get('available', 0)}")
                print(f"  Cost-MRP:  {stock['cost_price']}-{stock['mrp']}")
        else:
            print("[WARN] No stock data returned")
    else:
        print(f"[ERR] API Error: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("[ERR] Cannot connect to server")
    print("     Make sure FastAPI server is running:")
    print("     uvicorn main:app --reload")
except Exception as e:
    print(f"[ERR] Error: {str(e)[:100]}")

print("\n" + "="*70 + "\n")
