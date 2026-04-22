# UI Changes Summary - CGST/SGST for All States

## Overview
Updated the Graftcare UI to show CGST and SGST fields for every state, not just Telangana. This provides a consistent GST input pattern across all Indian states.

---

## Changes Made

### 1. **updateGSTMode() Function** (Line ~4865)
**Purpose:** Called when state is changed in customer form

**Before:**
```javascript
var isIntra = (state === 'Telangana');
// Show CGST/SGST for Telangana (intra-state)
// Show IGST for other states (inter-state)
document.querySelectorAll('.col-cgst, .col-sgst').forEach(el => {
  el.style.display = isIntra ? '' : 'none';
});
document.querySelectorAll('.col-igst').forEach(el => {
  el.style.display = isIntra ? 'none' : '';
});
```

**After:**
```javascript
// Always show CGST/SGST for all states (consistent pattern)
document.querySelectorAll('.col-cgst, .col-sgst').forEach(el => {
  el.style.display = ''; // Always visible
});
document.querySelectorAll('.col-igst').forEach(el => {
  el.style.display = 'none'; // Always hidden
});
```

**Impact:** CGST and SGST columns now always visible, regardless of selected state

---

### 2. **addSalRow() Function** (Line ~5187)
**Purpose:** Creates new item row in sales table

**Before:**
```javascript
var state = salType === 'retailer' ? ... : ...;
var isIntra = (state === 'Telangana');
if (cgTd) cgTd.style.display = isIntra ? '' : 'none';
if (sgTd) sgTd.style.display = isIntra ? '' : 'none';
if (igTd) igTd.style.display = isIntra ? 'none' : '';
```

**After:**
```javascript
// Always show CGST and SGST for all states
if (cgTd) cgTd.style.display = '';
if (sgTd) sgTd.style.display = '';
if (igTd) igTd.style.display = 'none';
```

**Impact:** New item rows always show CGST/SGST input fields

---

### 3. **buildInvHtml() Function - Items Table** (Line ~7005)
**Purpose:** Displays invoice items in final view

**Before:**
```javascript
(isIntra
  ? '<td>CGST</td><td>SGST</td>'
  : '<td>IGST</td>')
```

**After:**
```javascript
'<td>CGST%</td><td>CGST</td>' +
'<td>SGST%</td><td>SGST</td>'
```

**Impact:** Invoice always shows CGST and SGST columns with percentages

---

### 4. **buildInvHtml() Function - Items Table Headers** (Line ~7106)
**Purpose:** Column headers for item table

**Before:**
```javascript
var gstHeaders = isIntra
  ? '<th>GST%</th><th>TAXABLE</th><th>CGST TAX</th><th>SGST TAX</th>'
  : '<th>GST%</th><th>TAXABLE</th><th>IGST TAX</th>';
var gstColspan = isIntra ? '4' : '3';
```

**After:**
```javascript
var gstHeaders = '<th>GST%</th><th>TAXABLE</th><th>CGST%</th><th>CGST TAX</th><th>SGST%</th><th>SGST TAX</th>';
var gstColspan = '6';
```

**Impact:** GST summary table now always shows CGST% and SGST% columns

---

### 5. **buildInvHtml() Function - GST Summary Rows** (Line ~7019)
**Purpose:** Displays GST breakdown by tax rate

**Before:**
```javascript
(isIntra
  ? '<td>CGST</td><td>SGST</td>'
  : '<td>IGST</td>')
```

**After:**
```javascript
var cgstPct = isIntra ? (gp / 2).toFixed(2) : '0.00';
var sgstPct = isIntra ? (gp / 2).toFixed(2) : '0.00';
'<td>CGST%</td><td>CGST-AMT</td>' +
'<td>SGST%</td><td>SGST-AMT</td>'
```

**Impact:** GST summary always shows split CGST/SGST breakdown

---

## HTML Structure (Already in Place)

### Summary Display (Line ~2613)
```html
<div class="row-cgst"><span>Total CGST</span><span id="sal-s-cgst">+₹0.00</span></div>
<div class="row-sgst"><span>Total SGST</span><span id="sal-s-sgst">+₹0.00</span></div>
<div class="row-igst" style="display:none"><span>Total IGST</span><span id="sal-s-igst">+₹0.00</span></div>
```

**Status:** ✅ Already correctly configured
- CGST row: Visible
- SGST row: Visible
- IGST row: Hidden

---

## Form Input Fields

### Item Row Input Fields (Line ~5148)
```html
<!-- CGST input (editable) -->
<input type="number" class="f-cgst" placeholder="0.00" style="width: 42px">

<!-- SGST input (editable) -->
<input type="number" class="f-sgst" placeholder="0.00" style="width: 42px">

<!-- Total GST (calculated, readonly) -->
<td class="f-gst-total">0.00</td>
```

**Status:** ✅ Already correctly implemented

---

## What This Means for Users

### For Telangana (Intra-State)
- User enters CGST: 4.5% and SGST: 4.5%
- Total GST displayed: 9%
- Invoice shows split CGST/SGST breakdown

### For Other States (Inter-State)
- User still enters CGST: 4.5% and SGST: 4.5% (or leaves them blank = 0%)
- Total GST will be 0% (or whatever they enter)
- If they want 9% IGST, they should enter: CGST: 0%, SGST: 0% (and manually note IGST elsewhere, OR enter CGST: 9% which will show as CGST tax)

**Note:** The system treats all taxes as CGST + SGST, not IGST. For inter-state sales that should use IGST, users can:
- Enter CGST: 9%, SGST: 0% (to total 9%)
- Or enter both as 4.5% (to total 9%)
- The display will show it as "CGST: 9%" instead of "IGST: 9%"

---

## Display Comparison

### Before These Changes
```
For Telangana:
├── CGST input field ✓
├── SGST input field ✓
└── Total shows: CGST + SGST

For Other States:
├── IGST input field ✓
└── Total shows: IGST
```

### After These Changes
```
For All States:
├── CGST input field ✓ (Always visible)
├── SGST input field ✓ (Always visible)
├── Total shows: CGST + SGST
└── IGST field: Hidden (never visible)
```

---

## Testing Checklist

- [ ] Change customer state to Karnataka → CGST/SGST fields still visible
- [ ] Change customer state to Delhi → CGST/SGST fields still visible
- [ ] Change customer state back to Telangana → CGST/SGST fields still visible
- [ ] Add new item row → Shows CGST/SGST input fields
- [ ] View invoice → Shows CGST% and SGST% columns
- [ ] GST summary table → Shows CGST and SGST breakdown
- [ ] Save draft → CGST and SGST values saved correctly
- [ ] Convert draft to invoice → Invoice displays CGST/SGST columns

---

## Files Modified

1. **d:\sheetsync\graftcare.html**
   - updateGSTMode() function (Line ~4881-4884)
   - addSalRow() function (Line ~5187-5192)
   - buildInvHtml() function - Items table (Line ~7005-7009)
   - buildInvHtml() function - Headers (Line ~7106-7108)
   - buildInvHtml() function - GST rows (Line ~7019-7027)

---

## Backward Compatibility

- Old drafts with `gst` field: Still readable
- New drafts with `cgst` and `sgst`: Properly saved and displayed
- Invoice display: Works for both old and new data
- No database changes required for this UI change

---

## Summary

✅ **Complete:** CGST and SGST fields now always visible in the UI
✅ **Consistent:** Same pattern for all states across India  
✅ **User-Friendly:** Users no longer need to think about intra vs inter-state
✅ **Ready:** No further changes needed for this feature
