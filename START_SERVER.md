# 🚀 Quick Start - Run the Backend

## Step 1: Configure Supabase Credentials

Edit `backend/.env` and add your Supabase credentials:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-role-key
```

### How to Get Credentials:
1. Go to [supabase.com](https://supabase.com)
2. Sign in to your project
3. Go to **Settings → API**
4. Copy **Project URL** → paste to `SUPABASE_URL`
5. Copy **Service Role Secret** → paste to `SUPABASE_SERVICE_KEY`

---

## Step 2: Create Database Tables

### Option A: Using Supabase SQL Editor (Recommended)
1. Go to Supabase Dashboard → **SQL Editor**
2. Click **New Query**
3. Copy entire contents of `schema_complete.sql`
4. Paste into SQL editor
5. Click **Run**
6. Wait for "Success" message ✅

### Option B: Using Command Line
```bash
# Install psql (PostgreSQL client)
# Then run the schema
psql -h your-db-host -U postgres -f schema_complete.sql
```

---

## Step 3: Run Backend Server

From the `backend` directory:

```bash
# Activate virtual environment (if needed)
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies (one-time)
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

✅ Server is running!

---

## Step 4: Test the API

### Health Check
Open in your browser or use curl:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2026-04-22T10:30:00"
}
```

✅ API is working!

---

## Step 5: Open Frontend

### Option A: Direct Browser
1. Open `index.html` in your web browser
2. Or drag and drop into browser window

### Option B: Through Backend Server
1. Visit `http://localhost:8000` in browser
2. Frontend will load from FastAPI

---

## Step 6: Test Complete Workflow

### Create Test Data

#### 1. Create Vendor
- Go to **Vendors** tab
- Click **Add New Vendor**
- Fill in details:
  - Name: `Test Vendor`
  - Phone: `9999999999`
  - GSTIN: `27AAPFU1234H1Z0`
- Click **Save**
✅ Vendor created

#### 2. Create Product
- Go to **Products** tab
- Click **Add New Product**
- Fill in:
  - Name: `Dolo 650`
  - Company: `Cipla`
  - MRP: `30.00`
  - Cost Price: `10.00`
  - GST Rate: `18.00`
- Click **Save**
✅ Product created

#### 3. Create Purchase Invoice
- Go to **Purchase Invoices** tab
- Click **Add New Invoice**
- Select Vendor: `Test Vendor`
- Add Item:
  - Product: `Dolo 650`
  - Qty: `100`
  - Batch: `BATCH-001`
  - Expiry: Pick any future date
- Fill GST: `18` (auto-calculates SGST=9, CGST=9)
- Click **Save**
✅ Stock increases by 100

#### 4. Create Customer
- Go to **Customers** tab
- Click **Add New Customer**
- Fill:
  - Name: `Test Hospital`
  - Phone: `8888888888`
  - GSTIN: `27AAPFU5678H1Z0`
  - Type: `hospital`
- Click **Save**
✅ Customer created

#### 5. Create & Convert Draft
- Go to **Drafts** tab
- Click **New Draft**
- Select: `Test Hospital`
- Add Item: `Dolo 650`, Qty: `50`
- GST: `18%` (auto-calculates)
- Click **Save**
✅ Draft created (stock unchanged)

#### 6. Draft → Proforma
- Open the draft
- Click **Convert to Proforma**
✅ Now in Proformas (stock still unchanged)

#### 7. Proforma → Final Invoice
- Go to **Proformas** tab
- Open the proforma
- Click **Finalize to Invoice**
✅ Stock decreases by 50
✅ Invoice Number: `GCPS-2026-0001` (auto-generated)

#### 8. Check Dashboard
- Go to **Dashboard** tab
- Verify:
  - Vendors: 1
  - Products: 1
  - Customers: 1
  - Total Sales: 1
✅ All correct!

---

## Verify Data in Supabase

Open Supabase SQL Editor and run:

### Check Stock
```sql
SELECT product_id, SUM(change_qty) as current_stock 
FROM stock_ledger 
GROUP BY product_id;
```
Expected: `current_stock = 50` (100 - 50)

### Check Invoices
```sql
SELECT id, invoice_number, grand_total FROM invoices;
```
Expected: Shows `GCPS-2026-0001` with total

### Check Stock Ledger
```sql
SELECT * FROM stock_ledger ORDER BY created_at DESC;
```
Expected: Shows +100 (purchase) and -50 (sale)

---

## Common Issues & Solutions

### Issue: "Connection refused"
```
Error: Cannot connect to localhost:8000
```
**Solution:** Make sure backend server is running
```bash
uvicorn main:app --reload
```

### Issue: "Table doesn't exist"
```
Error: relation "vendors" does not exist
```
**Solution:** Run `schema_complete.sql` in Supabase SQL Editor

### Issue: "SUPABASE_URL or SUPABASE_SERVICE_KEY not found"
```
Error: Missing SUPABASE_URL or SUPABASE_SERVICE_KEY in .env file
```
**Solution:**
1. Edit `backend/.env`
2. Add your actual Supabase credentials
3. Restart backend server

### Issue: Frontend shows "Cannot reach API"
**Solution:**
1. Check if backend is running on port 8000
2. Check browser console for actual error
3. Make sure CORS is enabled (it is by default)

---

## API Testing

### Using cURL (Command Line)

#### Get All Vendors
```bash
curl http://localhost:8000/api/vendors
```

#### Create Vendor
```bash
curl -X POST http://localhost:8000/api/vendors \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Vendor",
    "phone": "1111111111",
    "gstin": "27AAPFU9999H1Z0"
  }'
```

#### Get Dashboard Stats
```bash
curl http://localhost:8000/api/dashboard
```

### Using Postman (GUI)
1. Download [Postman](https://www.postman.com/downloads/)
2. Import API endpoints
3. Test each endpoint

---

## Next Steps

1. ✅ Backend running
2. ✅ Database created
3. ✅ Frontend loaded
4. ✅ Test workflow complete
5. Next: Add more vendors/products and test complete workflows

---

## Documentation

- **API_DOCUMENTATION.md** - Complete API reference
- **DATABASE_STRUCTURE.md** - Database schema details
- **SETUP_GUIDE.md** - Detailed installation guide
- **README.md** - Project overview

---

## Running in Background (Windows)

To keep server running after closing terminal:

```bash
# Create a batch file: run_server.bat
@echo off
cd /d D:\sheetsync\backend
call venv\Scripts\activate
uvicorn main:app --reload
pause
```

Then double-click `run_server.bat`

---

**Status:** ✅ Ready to run!  
**Backend Port:** 8000  
**Frontend:** index.html  
**Database:** Supabase PostgreSQL  

Start the server now! 🚀
