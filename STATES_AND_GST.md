# GST Management - Simple Frontend Calculation

## Overview

**Simple GST calculation with user override:**
- User enters GST rate → Auto-calculates SGST = GST/2, CGST = GST/2
- User can manually override SGST/CGST at any time
- No database state lookup needed
- Calculation happens entirely in frontend

---

## GST Calculation Logic

### One Way to Enter GST:

#### **Enter GST Manually** (Frontend Only)
```
User enters GST: 18%
         ↓
Auto-calculated:
  SGST = 18 / 2 = 9%
  CGST = 18 / 2 = 9%
         ↓
User can manually override any value
  (Change SGST to 8%, GST auto-updates to 17%)
  (Change CGST to 10%, GST auto-updates to 18%)
```

### Auto-Calculation Function:
```javascript
function calculateGST(gstRate) {
  const gst = parseFloat(gstRate) || 0;
  const sgst = gst / 2;  // SGST = GST / 2
  const cgst = gst / 2;  // CGST = GST / 2
  
  return {
    gst: gst,
    sgst: sgst,
    cgst: cgst
  };
}

// Example:
// User enters GST: 18
// Auto-calculated:
//   SGST: 18 / 2 = 9%
//   CGST: 18 / 2 = 9%
//
// User can manually override SGST or CGST if needed
```

### Form Fields:
```
GST Rate:  [18] %         ← User enters manually
         ↓
SGST:      [9]   %        ← Auto-calculated (editable)
CGST:      [9]   %        ← Auto-calculated (editable)
```

### Amount Calculation:
```javascript
function calculateAmounts(taxableAmount, sgstRate, cgstRate) {
  const sgstAmount = (taxableAmount * sgstRate) / 100;
  const cgstAmount = (taxableAmount * cgstRate) / 100;
  const totalGst = sgstAmount + cgstAmount;
  const totalAmount = taxableAmount + totalGst;
  
  return {
    sgstAmount: sgstAmount,
    cgstAmount: cgstAmount,
    totalGst: totalGst,
    totalAmount: totalAmount
  };
}

// Example:
// Taxable Amount: ₹1000
// SGST Rate: 9% → ₹90
// CGST Rate: 9% → ₹90
// Total GST: ₹180
// Total Amount: ₹1180
```

---

## Frontend Implementation

### Add to main.js:
```javascript
function calculateGST(gstRate) {
  const gst = parseFloat(gstRate) || 0;
  return {
    gst: gst,
    sgst: gst / 2,
    cgst: gst / 2
  };
}

// When user enters GST - auto-calculate SGST/CGST
document.getElementById('gst-input').addEventListener('input', function(e) {
  const gstRate = parseFloat(e.target.value) || 0;
  const calculated = calculateGST(gstRate);
  
  document.getElementById('sgst-input').value = calculated.sgst.toFixed(2);
  document.getElementById('cgst-input').value = calculated.cgst.toFixed(2);
});

// Allow user to manually override SGST
document.getElementById('sgst-input').addEventListener('input', function(e) {
  const sgst = parseFloat(e.target.value) || 0;
  const cgst = parseFloat(document.getElementById('cgst-input').value) || 0;
  document.getElementById('gst-input').value = (sgst + cgst).toFixed(2);
});

// Allow user to manually override CGST
document.getElementById('cgst-input').addEventListener('input', function(e) {
  const sgst = parseFloat(document.getElementById('sgst-input').value) || 0;
  const cgst = parseFloat(e.target.value) || 0;
  document.getElementById('gst-input').value = (sgst + cgst).toFixed(2);
});
```

---

## Backend Implementation

### Python (FastAPI - main.py):
```python
def calculate_gst(gst_rate):
    """Auto-calculate SGST and CGST"""
    gst = float(gst_rate) if gst_rate else 0
    return {
        'gst': gst,
        'sgst': gst / 2,
        'cgst': gst / 2
    }

@app.post("/api/calculate-gst")
async def calculate_gst_endpoint(gst_rate: float):
    """Calculate SGST and CGST from GST rate"""
    return calculate_gst(gst_rate)
```

---

## Usage Examples

### Purchase Invoice:
```
Product: Dolo 650
Taxable Amount: ₹500
GST Rate: [18] %
  SGST: 9% = ₹45
  CGST: 9% = ₹45
Total: ₹590
```

### Sales Invoice:
```
Product: Aspirin 100 tablets
Taxable Amount: ₹1000
GST Rate: [5] %
  SGST: 2.5% = ₹25
  CGST: 2.5% = ₹25
Total: ₹1050
```

### Manual Override Example:
```
Product: Medicine XYZ
Taxable Amount: ₹2000
User enters GST: [18]%
  Auto-calc: SGST=9%, CGST=9%
User manually changes SGST to [8]%
  → GST auto-updates to 17% (8+9)
User manually changes CGST to [10]%
  → GST auto-updates to 18% (8+10)
```

---

## How It Works:

1. **User enters GST** → Frontend auto-calculates SGST=GST/2, CGST=GST/2
2. **User can override** → Change SGST or CGST manually
3. **GST recalculates** → GST = SGST + CGST (updates automatically)
4. **No database lookup** → All calculation in frontend, simple and fast

---

**Note:** This is a simplified approach with no state-wise complexity. Users have full control over GST/SGST/CGST values and can set them per transaction as needed.
