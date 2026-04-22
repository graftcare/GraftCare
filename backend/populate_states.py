"""
Populate the states table with all Indian states and union territories
"""

import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from supabase_client import supabase

print("\n" + "="*70)
print("POPULATING STATES TABLE WITH INDIAN STATES AND UTs")
print("="*70 + "\n")

# Complete list of Indian states and union territories
states_data = [
    # States (28)
    {"state_code": "AP", "state_name": "Andhra Pradesh"},
    {"state_code": "AR", "state_name": "Arunachal Pradesh"},
    {"state_code": "AS", "state_name": "Assam"},
    {"state_code": "BR", "state_name": "Bihar"},
    {"state_code": "CG", "state_name": "Chhattisgarh"},
    {"state_code": "GA", "state_name": "Goa"},
    {"state_code": "GJ", "state_name": "Gujarat"},
    {"state_code": "HR", "state_name": "Haryana"},
    {"state_code": "HP", "state_name": "Himachal Pradesh"},
    {"state_code": "JK", "state_name": "Jammu and Kashmir"},
    {"state_code": "JH", "state_name": "Jharkhand"},
    {"state_code": "KA", "state_name": "Karnataka"},
    {"state_code": "KL", "state_name": "Kerala"},
    {"state_code": "MP", "state_name": "Madhya Pradesh"},
    {"state_code": "MH", "state_name": "Maharashtra"},
    {"state_code": "MN", "state_name": "Manipur"},
    {"state_code": "ML", "state_name": "Meghalaya"},
    {"state_code": "MZ", "state_name": "Mizoram"},
    {"state_code": "NL", "state_name": "Nagaland"},
    {"state_code": "OR", "state_name": "Odisha"},
    {"state_code": "PB", "state_name": "Punjab"},
    {"state_code": "RJ", "state_name": "Rajasthan"},
    {"state_code": "SK", "state_name": "Sikkim"},
    {"state_code": "TN", "state_name": "Tamil Nadu"},
    {"state_code": "TG", "state_name": "Telangana"},
    {"state_code": "TR", "state_name": "Tripura"},
    {"state_code": "UP", "state_name": "Uttar Pradesh"},
    {"state_code": "UT", "state_name": "Uttarakhand"},
    {"state_code": "WB", "state_name": "West Bengal"},

    # Union Territories (8)
    {"state_code": "AN", "state_name": "Andaman and Nicobar Islands"},
    {"state_code": "CH", "state_name": "Chandigarh"},
    {"state_code": "DD", "state_name": "Dadra and Nagar Haveli and Daman and Diu"},
    {"state_code": "LA", "state_name": "Ladakh"},
    {"state_code": "LL", "state_name": "Lakshadweep"},
    {"state_code": "DL", "state_name": "Delhi"},
    {"state_code": "PY", "state_name": "Puducherry"},
]

print(f"Attempting to populate {len(states_data)} states...\n")

# First, check if table exists by trying to select from it
try:
    check_response = supabase.table("states").select("id", count="exact").execute()
    print("[INFO] States table already exists")
    existing_count = check_response.count if hasattr(check_response, 'count') else 0
    print(f"[INFO] Current records in states table: {existing_count}\n")
except Exception as e:
    print(f"[INFO] States table needs to be created: {str(e)[:50]}\n")

# Try to insert states
try:
    response = supabase.table("states").insert(states_data).execute()
    inserted = len(response.data) if response.data else 0
    print(f"[OK] Successfully inserted {inserted} states\n")
except Exception as e:
    error_msg = str(e)
    if "already exists" in error_msg or "duplicate" in error_msg.lower():
        print(f"[WARN] Some states already exist (duplicate key error)\n")
        print("       This is OK - states table is already populated\n")
    else:
        print(f"[ERR] Error inserting states: {error_msg[:100]}\n")

# Verify final count
print("="*70)
print("VERIFICATION")
print("="*70 + "\n")

try:
    response = supabase.table("states").select("*").order("state_name").execute()
    states = response.data if response.data else []

    print(f"Total states in database: {len(states)}\n")

    if states:
        print("States available:")
        for i, state in enumerate(states, 1):
            print(f"  {i:2}. {state['state_name']:45} ({state['state_code']})")

    print("\n" + "="*70)
    if len(states) >= 36:
        print("SUCCESS - All states and union territories are available!")
    else:
        print(f"WARNING - Only {len(states)} states found (expected 36)")
    print("="*70 + "\n")

except Exception as e:
    print(f"[ERR] Error verifying states: {str(e)[:80]}")
