# Graftcare - Complete Setup Guide

## Prerequisites

- Python 3.8 or higher
- Supabase account (free tier available at supabase.com)
- Git (optional, for version control)

---

## Step 1: Supabase Database Setup

### 1.1 Create Supabase Project
1. Go to [supabase.com](https://supabase.com)
2. Sign up or log in
3. Create a new project
4. Choose PostgreSQL database
5. Copy your **Project URL** and **Service Role Key** (from Settings → API)

### 1.2 Create Database Schema
1. Open SQL Editor in Supabase dashboard
2. Copy entire contents of `schema_complete.sql`
3. Paste into SQL Editor
4. Click "Run"
5. Wait for all 12 tables to be created

**Tables Created:**
- vendors
- products
- customers
- purchase_invoices
- purchase_items
- drafts
- draft_items
- proformas
- proforma_items
- invoices
- invoice_items
- stock_ledger

✅ Verify all tables exist in the "Tables" panel

---

## Step 2: Backend Setup

### 2.1 Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, create it:
```bash
pip install fastapi uvicorn supabase python-dotenv
pip freeze > requirements.txt
```

### 2.2 Configure Environment Variables
1. Copy `.env.example` to `.env`
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and fill in your Supabase credentials:
   ```
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_SERVICE_KEY=your-service-role-key-here
   ```

### 2.3 Verify Supabase Connection
```bash
python -c "from supabase_client import supabase; print('Connected!' if supabase else 'Failed')"
```

### 2.4 Run Backend Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
```
Uvicorn running on http://0.0.0.0:8000
Press ENTER to quit
```

✅ Test health check: `curl http://localhost:8000/health`

---

## Step 3: Frontend Setup

### 3.1 Required Files
Ensure these files exist in project root:
- `index.html` - Main HTML page
- `main.js` - Frontend JavaScript
- `main.css` - Styling

### 3.2 Open in Browser
1. Open `index.html` in your web browser
   ```bash
   # On Windows
   start index.html
   
   # On Mac
   open index.html
   
   # On Linux
   xdg-open index.html
   ```

2. Or navigate to: `http://localhost:8000` (if serving through FastAPI)

---

## Step 4: Test the Complete Workflow

### 4.1 Create a Vendor
1. Go to **Vendors** tab
2. Click **Add New Vendor**
3. Fill in details:
   - Name: "Test Vendor"
   - Phone: "9999999999"
   - GSTIN: "27AAPFU1234H1Z0"
   - City: "Mumbai"
4. Click **Save**

✅ Check Supabase: Vendors table should have 1 row

### 4.2 Create Products
1. Go to **Products** tab
2. Click **Add New Product**
3. Fill in:
   - Name: "Dolo 650"
   - Company: "Cipla"
   - MRP: 30.0
   - Cost Price: 10.0
   - GST Rate: 18.0
4. Click **Save**

✅ Check Supabase: Products table should have 1 row

### 4.3 Create Purchase Invoice
1. Go to **Purchase Invoices** tab
2. Click **Add New Invoice**
3. Select vendor (Test Vendor)
4. Add product (Dolo 650), qty 100, batch "BATCH-001", expiry date
5. Fill GST details (auto-calculates SGST/CGST as 18/2 = 9% each)
6. Click **Save**

✅ Stock increases by 100

### 4.4 Create Customer
1. Go to **Customers** tab
2. Click **Add New Customer**
3. Fill in:
   - Name: "Test Hospital"
   - Phone: "8888888888"
   - GSTIN: "27AAPFU5678H1Z0"
   - Type: "hospital"
4. Click **Save**

### 4.5 Create Draft Invoice
1. Go to **Drafts** tab
2. Click **New Draft**
3. Select customer (Test Hospital)
4. Add product (Dolo 650), qty 50
5. Fill GST: 18% (auto-calculates to SGST 9%, CGST 9%)
6. Click **Save**

✅ No stock change (still in draft)

### 4.6 Convert Draft → Proforma
1. Open the draft
2. Click **Convert to Proforma**
3. Review details

✅ Draft moves to Proformas, stock still unchanged

### 4.7 Finalize Proforma → Invoice
1. Go to **Proformas** tab
2. Open the proforma
3. Click **Finalize to Invoice**

✅ Stock decreases by 50
✅ Invoice number auto-generated: **GCPS-2026-0001**

### 4.8 Check Dashboard
1. Go to **Dashboard** tab
2. Verify:
   - Vendors: 1
   - Products: 1
   - Customers: 1
   - Total Sales: 1
   - Total Revenue: calculated correctly

---

## Step 5: Verify Complete Data Flow

### Stock Ledger Check
In Supabase SQL Editor, run:
```sql
SELECT * FROM stock_ledger ORDER BY created_at DESC;
```

Expected output:
```
| product_id | change_qty | reason | reference_id |
|------------|-----------|--------|--------------|
| uuid       | -50       | sale   | invoice_uuid |
| uuid       | +100      | purchase | pi_uuid    |
```

Current stock = 100 + (-50) = 50 ✅

### Invoice Verification
```sql
SELECT id, invoice_number, invoice_date, grand_total FROM invoices;
```

Should show:
```
| id | invoice_number | invoice_date | grand_total |
|----|----------------|--------------|-------------|
| uuid | GCPS-2026-0001 | 2026-04-22 | 5900.0 |
```

---

## API Testing

### Using cURL

#### Get All Vendors
```bash
curl http://localhost:8000/api/vendors
```

#### Create New Vendor
```bash
curl -X POST http://localhost:8000/api/vendors \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Vendor",
    "phone": "1111111111",
    "gstin": "27AAPFU9999H1Z0"
  }'
```

#### Get Product Stock
```bash
curl http://localhost:8000/api/stock/product-uuid
```

#### Get Dashboard Stats
```bash
curl http://localhost:8000/api/dashboard
```

See `API_DOCUMENTATION.md` for complete API reference.

---

## Troubleshooting

### Issue: "Connection refused" when running backend
**Solution:**
```bash
# Make sure Supabase URL and key are in .env
# Make sure Python dependencies are installed
pip install supabase python-dotenv fastapi uvicorn
```

### Issue: "Table doesn't exist" errors
**Solution:**
1. Go to Supabase SQL Editor
2. Run `schema_complete.sql` again
3. Verify all 12 tables exist

### Issue: Frontend can't reach backend
**Solution:**
1. Ensure backend is running: `uvicorn main:app --reload`
2. Check CORS settings (should allow "*" by default)
3. Verify backend is on port 8000
4. Check browser console for actual error message

### Issue: Stock not updating
**Solution:**
1. Check stock_ledger table for entries
2. Verify invoice was properly finalized (not just in proforma)
3. Check invoice_items table for correct qty values

---

## Project Structure

```
sheetsync/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── supabase_client.py      # Database functions
│   ├── .env                    # Environment variables (SECRET!)
│   ├── .env.example            # Template for .env
│   └── requirements.txt        # Python dependencies
├── index.html                  # Main HTML page
├── main.js                     # Frontend JavaScript
├── main.css                    # Styling
├── schema_complete.sql         # Database schema
├── DATABASE_STRUCTURE.md       # Database documentation
├── STATES_AND_GST.md          # GST calculation guide
├── API_DOCUMENTATION.md        # API reference
└── SETUP_GUIDE.md             # This file
```

---

## Key Production Checklist

- [ ] Supabase project created and schema imported
- [ ] `.env` file configured with Supabase credentials
- [ ] Backend dependencies installed
- [ ] Backend server running without errors
- [ ] Frontend loads without errors
- [ ] Health check passes: `curl http://localhost:8000/health`
- [ ] Can create vendors, products, customers
- [ ] Purchase invoice creates stock ledger entries
- [ ] Draft → Proforma conversion works
- [ ] Proforma → Invoice generates GCPS-YYYY-NNNN number
- [ ] Stock deduction works correctly
- [ ] Dashboard shows correct statistics

---

## Next Steps

1. **Add Authentication:** Add JWT or API key auth to backend
2. **Add File Upload:** Support CSV import for bulk data
3. **Add Reports:** Generate PDF invoices
4. **Add Notifications:** Email/SMS for order status
5. **Deploy:** Move to production server
6. **Backup:** Set up automated database backups

---

## Support

For issues, check:
- Backend logs for error messages
- Supabase SQL Editor for data
- Browser console for frontend errors
- `API_DOCUMENTATION.md` for endpoint details

---

**Status:** ✅ Production Ready
**Last Updated:** 2026-04-22
**Version:** 1.0.0
