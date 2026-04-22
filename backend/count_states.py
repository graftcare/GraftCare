import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from supabase_client import supabase

print("\n" + "="*70)
print("COUNTING STATES IN DATABASE")
print("="*70 + "\n")

try:
    response = supabase.table("states").select("*", count="exact").execute()
    count = response.count if hasattr(response, 'count') else len(response.data)
    
    print(f"Total states in database: {count}")
    
    if count > 0:
        print(f"\nFetching all states...")
        response = supabase.table("states").select("state_code, state_name").order("state_name").execute()
        states = response.data if response.data else []
        
        print(f"States retrieved: {len(states)}\n")
        
        for i, state in enumerate(states, 1):
            print(f"  {i:2}. {state['state_name']:45} ({state['state_code']})")
    
except Exception as e:
    print(f"Error: {str(e)[:150]}")

print("\n" + "="*70 + "\n")
