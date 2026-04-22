import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from supabase_client import supabase

print("\n" + "="*70)
print("VERIFYING STATES TABLE WITH RATES")
print("="*70 + "\n")

try:
    response = supabase.table("states").select("*").limit(5).execute()
    states = response.data if response.data else []
    
    if states:
        print("Sample states with rates:")
        for state in states:
            print(f"  {state['state_name']:40} - SGST: {state.get('sgst_rate', 'N/A')}% | CGST: {state.get('cgst_rate', 'N/A')}%")
        print(f"\n[OK] States table has {len(states)} records with rates")
    else:
        print("[ERR] No states found")
        
except Exception as e:
    print(f"[ERR] Error: {str(e)[:100]}")

print("\n" + "="*70 + "\n")
