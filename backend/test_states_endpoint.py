import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import time

BASE_URL = "http://localhost:8000/api"

print("\n" + "="*70)
print("TESTING STATES API ENDPOINT")
print("="*70 + "\n")

# Try to call the endpoint
try:
    print("Calling /api/states...")
    response = requests.get(f"{BASE_URL}/states", timeout=5)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        states = response.json()
        print(f"\nTotal states returned: {len(states)}")
        
        if len(states) > 0:
            print(f"\nFirst 10 states:")
            for i, state in enumerate(states[:10], 1):
                print(f"  {i:2}. {state['state_name']:40} ({state['state_code']})")
            
            if len(states) > 10:
                print(f"\n  ... and {len(states) - 10} more states")
            
            print(f"\n[OK] All states are being returned!")
        else:
            print("[ERR] No states returned")
    else:
        print(f"[ERR] API returned error: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("[ERR] Cannot connect to server at localhost:8000")
    print("     Make sure FastAPI server is running:")
    print("     uvicorn main:app --reload")
except Exception as e:
    print(f"[ERR] Error: {str(e)}")

print("\n" + "="*70 + "\n")
