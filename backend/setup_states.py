"""
Setup states table - create table and populate with data
This script creates the states table and populates all Indian states
"""

import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from supabase_client import supabase
import time

print("\n" + "="*70)
print("SETTING UP STATES TABLE")
print("="*70 + "\n")

# All Indian states and union territories
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

print("Step 1: Creating states table...\n")

# Use RPC or direct API call to create table
sql_create_table = """
CREATE TABLE IF NOT EXISTS states (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    state_code VARCHAR(2) NOT NULL UNIQUE,
    state_name VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_states_code ON states(state_code);
CREATE INDEX IF NOT EXISTS idx_states_name ON states(state_name);
"""

print("[INFO] Please run the following SQL in Supabase SQL Editor:\n")
print(sql_create_table)
print("\nOr use Supabase Dashboard > SQL Editor to paste and execute the above SQL.\n")
print("="*70)
print("After creating the table, run: python populate_states.py")
print("="*70 + "\n")

# Try to insert states anyway (in case table was created manually)
print("Step 2: Attempting to populate states...\n")

try:
    response = supabase.table("states").insert(states_data).execute()
    inserted = len(response.data) if response.data else 0
    print(f"[OK] Successfully inserted {inserted} states\n")
    success = True
except Exception as e:
    error_msg = str(e)
    if "does not exist" in error_msg.lower() or "could not find" in error_msg.lower():
        print(f"[ERR] States table does not exist yet\n")
        print("      Please create the table first using the SQL above\n")
        success = False
    elif "already exists" in error_msg or "duplicate" in error_msg.lower():
        print(f"[WARN] Some/all states already exist\n")
        success = True
    else:
        print(f"[ERR] Error: {error_msg[:100]}\n")
        success = False

# Verify
if success:
    print("="*70)
    print("VERIFICATION")
    print("="*70 + "\n")

    try:
        response = supabase.table("states").select("*", count="exact").order("state_name").execute()
        states = response.data if response.data else []
        count = response.count if hasattr(response, 'count') else len(states)

        print(f"Total states in database: {count}\n")

        if states and len(states) > 0:
            print("States available:")
            for i, state in enumerate(states[:10], 1):
                print(f"  {i:2}. {state['state_name']:45} ({state['state_code']})")
            if len(states) > 10:
                print(f"  ... and {len(states) - 10} more states")

        print("\n" + "="*70)
        if count >= 36:
            print("SUCCESS - All states and union territories are available!")
        else:
            print(f"Partial - {count} states found (expected 36)")
        print("="*70 + "\n")

    except Exception as e:
        print(f"[ERR] Error verifying: {str(e)[:80]}")
