import requests

BASE_URL = "http://localhost:8000/api"

print("\n" + "="*60)
print("TESTING NEW ENDPOINTS")
print("="*60 + "\n")

# Test invoice number generation
print("1. Testing /api/next-invoice-number/retail")
response = requests.get(f"{BASE_URL}/next-invoice-number/retail")
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}\n")

print("2. Testing /api/next-invoice-number/purchase")
response = requests.get(f"{BASE_URL}/next-invoice-number/purchase")
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}\n")

# Test expiry endpoint
print("3. Testing /api/expiry")
response = requests.get(f"{BASE_URL}/expiry")
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"   Total records: {len(data)}")
    if len(data) > 0:
        print(f"   Sample: {data[0]}")
else:
    print(f"   Error: {response.json()}")

print("\n" + "="*60)
print("✓ NEW ENDPOINTS TEST COMPLETE")
print("="*60 + "\n")
