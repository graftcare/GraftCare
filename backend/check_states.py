import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from supabase_client import supabase

print("\n" + "="*70)
print("CHECKING CURRENT STATES IN DATABASE")
print("="*70 + "\n")

try:
    response = supabase.table("states").select("*").order("state_name").execute()
    states = response.data if response.data else []
    
    print(f"Total states: {len(states)}\n")
    
    if states:
        print("Current states:")
        for state in states:
            print(f"  - {state['state_name']} (Code: {state['state_code']})")
    else:
        print("No states found in database")
        
except Exception as e:
    print(f"Error: {str(e)}")

print("\n" + "="*70 + "\n")
