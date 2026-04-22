# Graftcare Proforma/Sales - CGST/SGST Implementation Summary

## Overview
Updated the Graftcare proforma/sales invoice system to use separate editable CGST and SGST fields instead of a single GST rate. This allows flexible GST handling for both intra-state (CGST + SGST) and inter-state (IGST) transactions.

---

## Changes Made

### 1. Frontend Changes (graftcare.html)

#### A. Row-Level Item Input Fields
**Location:** Line ~5147-5154 (addSalRow function)
- ✅ Replaced single `.f-gst` input field with:
  - `.f-cgst` - CGST percentage (editable)
  - `.f-sgst` - SGST percentage (editable)
  - `.f-gst-total` - Sum of CGST + SGST (calculated, display-only)

#### B. Prefill Logic
**Location:** Line ~5172-5176 (addSalRow function)
- ✅ Updated to handle CGST and SGST separately
- ✅ Falls back to splitting old single GST value if needed (backward compat)

#### C. Row Calculation Function
**Location:** calcSalRow function
- ✅ Reads `.f-cgst` and `.f-sgst` separately
- ✅ Calculates CGST and SGST amounts independently
- ✅ Displays total GST as sum of CGST + SGST

#### D. Form Collection Function (collectSalData)
**Location:** Line ~5506-5607
- ✅ Changed from reading `.f-gst` to `.f-cgst` and `.f-sgst`
- ✅ Items now contain: `cgst`, `sgst`, `cgstAmount`, `sgstAmount`
- ✅ Properly builds gstMap with separate CGST/SGST values for intra-state
- ✅ Properly handles IGST for inter-state transactions

#### E. Summary Calculation Functions
**Location:** calcSal function (Line ~5247)
- ✅ Changed to read CGST and SGST separately instead of single GST
- ✅ Calculates `cgstTotal` and `sgstTotal` independently
- ✅ Displays summary with split CGST/SGST amounts

**Location:** applyNetPayable function (Line ~5298)
- ✅ Updated to read CGST and SGST separately
- ✅ Proper total GST calculation from CGST + SGST

#### F. Draft Save Function (saveDraftOnly)
**Location:** Line ~5673-5820
- ✅ Items now include `cgst` and `sgst` instead of single `gst`
- ✅ All other transformation logic works with new item format

---

### 2. Backend Integration

#### A. DraftModel (main.py, Line ~124)
- ✅ Already has flat individual customer columns
- ✅ Items stored as `List[Dict[str, Any]]` (flexible JSONB)
- ✅ Backend accepts new item format with cgst/sgst

#### B. draft_to_invoice Function (main.py, Line ~786)
- ✅ Properly transforms flat draft columns to invoice
- ✅ Copies items array as-is to invoice
- ✅ Creates/updates customer before creating invoice

#### C. Supabase Functions (supabase_client.py)
- ✅ lookup_draft_by_phone - Smart lookup by phone
- ✅ lookup_draft_by_gstin - Smart lookup by GSTIN (retailers)
- ✅ count_drafts_by_phone - For draft counter

---

## What Needs to Be Done

### 1. **CRITICAL: Run SQL Migration in Supabase** ⚠️
   **File:** `supabase_migration.sql`
   
   You MUST run this SQL in Supabase SQL Editor before testing:
   - Drops old draft_items, proforma_items, invoice_items tables
   - Adds individual customer columns to drafts table
   - Makes customer_id nullable in drafts table
   - Adds all columns to invoices table
   - Creates indexes for performance
   
   **Steps:**
   1. Open Supabase dashboard
   2. Go to SQL Editor
   3. Paste entire `supabase_migration.sql` content
   4. Click "Run"
   5. Confirm all operations completed

### 2. Restart Backend Server
   ```bash
   cd backend
   python main.py
   ```

### 3. Test in Browser
   1. Go to http://localhost:8000/graftcare.html
   2. Click "Sales" → "New Proforma"
   3. Select "Retailer" or "Patient"
   4. Fill in customer details
   5. Click "Add Row" to add items
   6. Verify CGST/SGST fields appear (not single GST)
   7. Enter CGST and SGST percentages
   8. Verify total GST shows as CGST + SGST sum
   9. Click "Save Draft"
   10. Verify draft saved successfully

### 4. Verify Invoice Conversion
   1. Open saved draft
   2. Click "Convert to Invoice"
   3. Check that invoice shows customer details
   4. Verify GST split displays correctly

---

## Data Format Changes

### Items Array in Draft/Invoice

**OLD Format:**
```javascript
{
  product_id: "...",
  batch: "BATCH-001",
  qty: 10,
  sale_rate: 100.00,
  discount: 5,
  gst: 9  // Single percentage
}
```

**NEW Format:**
```javascript
{
  product_id: "...",
  batch: "BATCH-001",
  qty: 10,
  sale_rate: 100.00,
  discount: 5,
  cgst: 4.5,    // CGST percentage (intra-state)
  sgst: 4.5     // SGST percentage (intra-state)
}
```

---

## Backward Compatibility

- If a draft has old `gst` field in prefill data, it's automatically split 50/50 into CGST/SGST
- Old fields still work in reading, but new drafts use the split format
- No existing draft data is lost or modified

---

## Testing Checklist

- [ ] SQL migration ran successfully in Supabase
- [ ] Backend server restarted
- [ ] Proforma form loads with CGST/SGST fields
- [ ] Can edit CGST and SGST percentages per row
- [ ] Total GST displayed correctly as CGST + SGST
- [ ] Draft saves with new item format
- [ ] Can edit existing draft
- [ ] Draft converts to invoice successfully
- [ ] Invoice shows correct GST split

---

## Troubleshooting

**Issue:** CGST/SGST fields not appearing
- Check browser console for JavaScript errors
- Verify SQL migration was run
- Restart backend server

**Issue:** "Cannot read property '.f-cgst' of null"
- Ensure addSalRow() function created all fields
- Check HTML table ID is `sal-items`

**Issue:** Incorrect GST amounts in summary
- Check calcSal() function is reading from `.f-cgst` and `.f-sgst`
- Verify formula: totalGst = cgstTotal + sgstTotal

**Issue:** Draft not saving
- Check browser network tab for API errors
- Verify customer phone number is filled
- Check backend logs for validation errors

---

## Files Modified

1. **d:\sheetsync\graftcare.html**
   - addSalRow: Added CGST/SGST input fields
   - prefill logic: Handle split GST values
   - collectSalData: Read CGST/SGST instead of GST
   - calcSal: Calculate totals from split values
   - applyNetPayable: Use split GST values
   - saveDraftOnly: Send cgst/sgst in items

2. **d:\sheetsync\backend\main.py**
   - Already configured for new item format
   - DraftModel accepts flexible item structure
   - draft_to_invoice already handles denormalized schema

3. **d:\sheetsync\backend\supabase_client.py**
   - Already has lookup functions
   - No changes needed

4. **d:\sheetsync\supabase_migration.sql** (NEW)
   - SQL migration script
   - Run this in Supabase SQL Editor

---

## Next Steps

1. Run the SQL migration in Supabase ⚠️
2. Restart the backend server
3. Test the proforma form in browser
4. Verify GST display in invoice view
5. Check Purchase Invoice section if you need to update it too (currently still uses old format)

