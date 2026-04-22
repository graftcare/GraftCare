import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from supabase_client import supabase

print("\n" + "="*70)
print("CHECKING STATES TABLE SCHEMA AND DATA")
print("="*70 + "\n")

try:
    response = supabase.table("states").select("*").limit(1).execute()
    
    if response.data:
        state = response.data[0]
        print("State record structure:")
        for key in state.keys():
            value = state[key]
            print(f"  - {key}: {value} ({type(value).__name__})")
        
        print("\nChecking if rates exist:")
        has_sgst = 'sgst_rate' in state
        has_cgst = 'cgst_rate' in state
        print(f"  SGST rate column: {'YES' if has_sgst else 'NO'}")
        print(f"  CGST rate column: {'YES' if has_cgst else 'NO'}")
        
        if has_sgst:
            print(f"  SGST rate value: {state['sgst_rate']}")
        if has_cgst:
            print(f"  CGST rate value: {state['cgst_rate']}")
    else:
        print("No states found")
        
except Exception as e:
    print(f"Error: {str(e)[:150]}")

print("\n" + "="*70 + "\n")
