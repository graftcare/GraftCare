import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from supabase_client import supabase

print("\n" + "="*70)
print("CHECKING VENDORS IN DATABASE")
print("="*70 + "\n")

try:
    response = supabase.table("vendors").select("id, name, gstin, phone").execute()
    vendors = response.data if response.data else []
    
    print(f"Total vendors: {len(vendors)}\n")
    
    if vendors:
        for i, vendor in enumerate(vendors, 1):
            print(f"{i}. {vendor['name']}")
            print(f"   GSTIN: {vendor.get('gstin', 'N/A')}")
            print(f"   Phone: {vendor.get('phone', 'N/A')}")
            print(f"   ID: {vendor['id']}\n")
    else:
        print("No vendors found in database")
        
except Exception as e:
    print(f"Error: {str(e)[:150]}")

print("="*70 + "\n")
