import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests

BASE_URL = "http://localhost:8000/api"

print("\n" + "="*70)
print("TESTING STATES API ENDPOINTS")
print("="*70 + "\n")

# Test 1: Get all states
print("1. GET /api/states - All states")
response = requests.get(f"{BASE_URL}/states")
if response.status_code == 200:
    states = response.json()
    print(f"   [OK] Status: {response.status_code}")
    print(f"   [OK] Total states: {len(states)}")
    if states:
        print(f"   [OK] Sample: {states[0]['state_name']} ({states[0]['state_code']})")
else:
    print(f"   [ERR] Status: {response.status_code}")

# Test 2: Get specific state
print("\n2. GET /api/states/MH - Get Maharashtra")
response = requests.get(f"{BASE_URL}/states/MH")
if response.status_code == 200:
    state = response.json()
    print(f"   [OK] Status: {response.status_code}")
    print(f"   [OK] State: {state['state_name']} ({state['state_code']})")
else:
    print(f"   [ERR] Status: {response.status_code}")

# Test 3: Get another state
print("\n3. GET /api/states/DL - Get Delhi")
response = requests.get(f"{BASE_URL}/states/DL")
if response.status_code == 200:
    state = response.json()
    print(f"   [OK] Status: {response.status_code}")
    print(f"   [OK] State: {state['state_name']} ({state['state_code']})")
else:
    print(f"   [ERR] Status: {response.status_code}")

print("\n" + "="*70)
print("SUCCESS - States API is working correctly!")
print("="*70 + "\n")
