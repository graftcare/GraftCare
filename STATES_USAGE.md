# 🗺️ States Implementation Guide

## Overview

Indian states are now available throughout the application. States can be:
- Loaded from `states.js` (frontend)
- Fetched via `/api/states` (backend API)
- Selected in vendor and customer forms

---

## Frontend Usage

### 1. Auto-Initialize All State Dropdowns

Any `<select>` element with `data-type="state-select"` will automatically populate:

```html
<select id="vendor-state" data-type="state-select">
  <!-- Will be auto-populated -->
</select>
```

### 2. Manually Populate Specific Dropdown

```javascript
// Populate specific dropdown
populateStates('vendor-state', '-- Select State --');
populateStates('customer-state', '-- Choose Your State --');
```

### 3. Get State Name from Code

```javascript
const stateName = getStateName('MH');
console.log(stateName); // Output: Maharashtra
```

### 4. Get State Code from Name

```javascript
const stateCode = getStateCode('Maharashtra');
console.log(stateCode); // Output: MH
```

---

## Backend API Usage

### Get All States

```bash
curl http://localhost:8000/api/states
```

**Response:**
```json
[
  {"code": "AP", "name": "Andhra Pradesh"},
  {"code": "AR", "name": "Arunachal Pradesh"},
  ...
  {"code": "DL", "name": "Delhi"}
]
```

### Vendor Form Example

```html
<select id="vendor-state" data-type="state-select">
  <!-- Auto-populated with all 36 states -->
</select>

<select id="buyer-state" data-type="state-select">
  <!-- Separate dropdown for buyer's state -->
</select>
```

### Get Selected State

```javascript
const vendorState = document.getElementById('vendor-state').value; // Returns: "TG"
const buyerState = document.getElementById('buyer-state').value;   // Returns: "MH"

// Send to backend
fetch('/api/vendors', {
  method: 'POST',
  body: JSON.stringify({
    name: "Gaudev and Co",
    state: vendorState,  // State code like "TG"
    city: "Hyderabad"
  })
});
```

---

## All 36 States Available

**States:** AP, AR, AS, BR, CG, GA, GJ, HR, HP, JK, JH, KA, KL, MP, MH, MN, ML, MZ, NL, OR, PB, RJ, SK, TN, TG, TR, UP, UT, WB

**Union Territories:** AN, CH, DD, LA, LL, DL, PY

---

## Form Fields with States

When filling Purchase Invoice or Vendor forms:

```
Vendor State: [Dropdown with all states] ✅
Your State (Buyer): [Dropdown with all states] ✅
```

Just click the dropdown and select from the list!

---

**Status:** ✅ States fully integrated and ready to use!
