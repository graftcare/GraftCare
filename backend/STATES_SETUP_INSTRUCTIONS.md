# States Table Setup Instructions

## Problem
The `states` table is missing from your Supabase database, which is why the vendor/purchase invoice form shows missing states.

## Solution

### Step 1: Open Supabase SQL Editor
1. Go to your Supabase Dashboard
2. Click on **SQL Editor** in the left sidebar
3. Click **New Query**

### Step 2: Copy and Execute the SQL

Copy the entire contents of `complete_states_setup.sql` and paste it into the SQL editor, then click **Run**.

This will:
- ✅ Create the `states` table
- ✅ Create indexes for faster lookups
- ✅ Insert all 36 Indian states and union territories

### Step 3: Verify

After execution, you should see output like:
```
total_states | unique_codes
     36      |      36
```

And a list of all states ordered by name.

## Available States (36 Total)

### States (28)
1. Andhra Pradesh (AP)
2. Arunachal Pradesh (AR)
3. Assam (AS)
4. Bihar (BR)
5. Chhattisgarh (CG)
6. Goa (GA)
7. Gujarat (GJ)
8. Haryana (HR)
9. Himachal Pradesh (HP)
10. Jammu and Kashmir (JK)
11. Jharkhand (JH)
12. Karnataka (KA)
13. Kerala (KL)
14. Madhya Pradesh (MP)
15. Maharashtra (MH)
16. Manipur (MN)
17. Meghalaya (ML)
18. Mizoram (MZ)
19. Nagaland (NL)
20. Odisha (OR)
21. Punjab (PB)
22. Rajasthan (RJ)
23. Sikkim (SK)
24. Tamil Nadu (TN)
25. Telangana (TG)
26. Tripura (TR)
27. Uttar Pradesh (UP)
28. Uttarakhand (UT)
29. West Bengal (WB)

### Union Territories (8)
1. Andaman and Nicobar Islands (AN)
2. Chandigarh (CH)
3. Dadra and Nagar Haveli and Daman and Diu (DD)
4. Delhi (DL)
5. Ladakh (LA)
6. Lakshadweep (LL)
7. Puducherry (PY)

## API Endpoints

Once the states table is populated, you can use these endpoints:

### Get all states
```
GET /api/states
```
Response:
```json
[
  {
    "id": "uuid",
    "state_code": "MH",
    "state_name": "Maharashtra",
    "created_at": "2026-04-22..."
  },
  ...
]
```

### Get state by code
```
GET /api/states/MH
```

## Testing

After setup, refresh your UI and try filling a vendor purchase invoice again. The states dropdown should now show all states.

## Troubleshooting

If you still don't see states after setup:
1. **Refresh the browser** - Clear cache (Ctrl+Shift+Delete) and reload
2. **Restart FastAPI server** - Run `uvicorn main:app --reload`
3. **Check Supabase** - Verify states are in the database: `SELECT COUNT(*) FROM states;`

## Files for Reference

- `complete_states_setup.sql` - Complete SQL script to run
- `populate_states.py` - Python script to populate (use after table creation)
- `setup_states.py` - Setup guide and verification script
