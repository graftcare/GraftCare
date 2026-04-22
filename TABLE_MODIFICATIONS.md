# Supabase Table Modifications Required

## Summary
The current schema uses separate `draft_items`, `proforma_items`, and `invoice_items` tables. We need to:
1. **DROP** the old item tables (no longer needed)
2. **ADD** individual customer columns to `drafts` table
3. **ADD** individual customer columns to `invoices` table
4. **ADD** items as JSONB array to both tables

---

## DRAFTS Table Modifications

### OLD STRUCTURE
```
drafts
├── id (UUID)
├── customer_id (UUID) → customers
├── subtotal (NUMERIC)
├── total_gst (NUMERIC)
├── discount_amount (NUMERIC)
├── grand_total (NUMERIC)
├── notes (TEXT)
├── created_at
└── updated_at
```
Items were stored in separate `draft_items` table

### NEW STRUCTURE
```
drafts
├── id (UUID) - PRIMARY KEY
├── customer_id (UUID) - NOW NULLABLE (optional, only for reference)
├── type (VARCHAR) - 'patient' or 'retailer'
├── draft_counter (INTEGER) - auto-incrementing counter per customer
│
├── COMMON CUSTOMER COLUMNS
├── customer_name (VARCHAR 255)
├── customer_phone (VARCHAR 20)
├── customer_address (TEXT)
├── customer_city (VARCHAR 100)
├── customer_pincode (VARCHAR 10)
├── customer_state (VARCHAR 100)
├── customer_door_number (VARCHAR 100)
│
├── RETAILER-SPECIFIC COLUMNS
├── customer_gstin (VARCHAR 50)
├── customer_dl1 (VARCHAR 100)
├── customer_dl2 (VARCHAR 100)
│
├── PATIENT-SPECIFIC COLUMNS
├── customer_age (VARCHAR 10)
├── customer_gender (VARCHAR 20)
├── customer_doctor_name (VARCHAR 255)
├── customer_hospital_name (VARCHAR 255)
├── customer_doctor_phone (VARCHAR 20)
├── customer_is_member (BOOLEAN)
├── customer_member_id (VARCHAR 100)
│
├── TOTALS
├── subtotal (NUMERIC)
├── total_gst (NUMERIC)
├── discount_amount (NUMERIC)
├── grand_total (NUMERIC)
├── notes (TEXT)
│
├── ITEMS (NEW - JSONB ARRAY)
├── items (JSONB) - Array of item objects
│   └── Each item contains:
│       ├── product_id (UUID)
│       ├── batch (TEXT)
│       ├── expiry (DATE)
│       ├── qty (INTEGER)
│       ├── mrp (NUMERIC)
│       ├── sale_rate (NUMERIC)
│       ├── discount (NUMERIC)
│       ├── cgst (NUMERIC) - CGST percentage
│       ├── sgst (NUMERIC) - SGST percentage
│       └── [other fields]
│
├── created_at (TIMESTAMPTZ)
└── updated_at (TIMESTAMPTZ)
```

### SQL Changes for DRAFTS
```sql
-- 1. Make customer_id nullable
ALTER TABLE drafts ALTER COLUMN customer_id DROP NOT NULL;

-- 2. Add type and counter
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS type VARCHAR(20) DEFAULT 'patient';
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS draft_counter INTEGER DEFAULT 1;

-- 3. Add common customer columns
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_name VARCHAR(255);
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_phone VARCHAR(20);
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_address TEXT;
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_city VARCHAR(100);
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_pincode VARCHAR(10);
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_state VARCHAR(100);
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_door_number VARCHAR(100);

-- 4. Add retailer-specific columns
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_gstin VARCHAR(50);
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_dl1 VARCHAR(100);
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_dl2 VARCHAR(100);

-- 5. Add patient-specific columns
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_age VARCHAR(10);
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_gender VARCHAR(20);
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_doctor_name VARCHAR(255);
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_hospital_name VARCHAR(255);
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_doctor_phone VARCHAR(20);
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_is_member BOOLEAN DEFAULT FALSE;
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_member_id VARCHAR(100);

-- 6. Add items as JSONB array
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS items JSONB DEFAULT '[]'::jsonb;

-- 7. Create indexes for lookups
CREATE INDEX IF NOT EXISTS idx_drafts_phone ON drafts(customer_phone);
CREATE INDEX IF NOT EXISTS idx_drafts_gstin ON drafts(customer_gstin);
CREATE INDEX IF NOT EXISTS idx_drafts_type ON drafts(type);
```

---

## INVOICES Table Modifications

### OLD STRUCTURE
```
invoices
├── id (UUID)
├── customer_id (UUID) → customers
├── invoice_date (DATE)
├── subtotal (NUMERIC)
├── total_gst (NUMERIC)
├── discount_amount (NUMERIC)
├── grand_total (NUMERIC)
├── payment_mode (TEXT)
├── notes (TEXT)
├── created_at
└── updated_at
```
Items were stored in separate `invoice_items` table

### NEW STRUCTURE
```
invoices
├── id (UUID) - PRIMARY KEY
├── customer_id (UUID) - References customers (for finalized invoices)
├── invoice_no (VARCHAR 50) - Unique invoice number: INV-YYYYMMDD-XXXX
├── invoice_date (DATE)
├── type (VARCHAR) - 'patient' or 'retailer'
│
├── DENORMALIZED CUSTOMER COLUMNS (copy from draft)
├── customer_name (VARCHAR 255)
├── customer_phone (VARCHAR 20)
├── customer_address (TEXT)
├── customer_city (VARCHAR 100)
├── customer_pincode (VARCHAR 10)
├── customer_state (VARCHAR 100)
├── customer_door_number (VARCHAR 100)
├── customer_gstin (VARCHAR 50)
├── customer_dl1 (VARCHAR 100)
├── customer_dl2 (VARCHAR 100)
├── customer_age (VARCHAR 10)
├── customer_gender (VARCHAR 20)
├── customer_doctor_name (VARCHAR 255)
├── customer_hospital_name (VARCHAR 255)
├── customer_doctor_phone (VARCHAR 20)
├── customer_is_member (BOOLEAN)
├── customer_member_id (VARCHAR 100)
│
├── TOTALS
├── subtotal (NUMERIC)
├── total_gst (NUMERIC)
├── discount_amount (NUMERIC)
├── grand_total (NUMERIC)
├── payment_mode (TEXT)
├── notes (TEXT)
│
├── ITEMS (NEW - JSONB ARRAY)
├── items (JSONB) - Array of finalized items
│   └── Each item contains:
│       ├── product_id (UUID)
│       ├── batch (TEXT)
│       ├── expiry (DATE)
│       ├── qty (INTEGER)
│       ├── mrp (NUMERIC)
│       ├── sale_rate (NUMERIC)
│       ├── discount (NUMERIC)
│       ├── cgst (NUMERIC)
│       ├── sgst (NUMERIC)
│       └── [other fields]
│
├── created_at (TIMESTAMPTZ)
└── updated_at (TIMESTAMPTZ)
```

### SQL Changes for INVOICES
```sql
-- 1. Add invoice number and type
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS invoice_no VARCHAR(50);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS type VARCHAR(20) DEFAULT 'patient';

-- 2. Add all common customer columns
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_name VARCHAR(255);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_phone VARCHAR(20);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_address TEXT;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_city VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_pincode VARCHAR(10);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_state VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_door_number VARCHAR(100);

-- 3. Add retailer-specific columns
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_gstin VARCHAR(50);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_dl1 VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_dl2 VARCHAR(100);

-- 4. Add patient-specific columns
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_age VARCHAR(10);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_gender VARCHAR(20);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_doctor_name VARCHAR(255);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_hospital_name VARCHAR(255);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_doctor_phone VARCHAR(20);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_is_member BOOLEAN DEFAULT FALSE;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_member_id VARCHAR(100);

-- 5. Add items as JSONB array
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS items JSONB DEFAULT '[]'::jsonb;

-- 6. Create indexes
CREATE INDEX IF NOT EXISTS idx_invoices_phone ON invoices(customer_phone);
CREATE INDEX IF NOT EXISTS idx_invoices_gstin ON invoices(customer_gstin);
CREATE INDEX IF NOT EXISTS idx_invoices_type ON invoices(type);
CREATE INDEX IF NOT EXISTS idx_invoices_number ON invoices(invoice_no);
```

---

## TABLES TO DROP

These tables are no longer needed (items are now in JSONB):

```sql
DROP TABLE IF EXISTS invoice_items CASCADE;
DROP TABLE IF EXISTS proforma_items CASCADE;
DROP TABLE IF EXISTS draft_items CASCADE;
```

---

## CUSTOMERS Table (No Changes)

The customers table remains unchanged. It only gets records when a draft is converted to invoice.

```
customers
├── id (UUID)
├── name (TEXT)
├── phone (TEXT)
├── gstin (TEXT)
├── customer_type (TEXT) - 'retailer' or 'patient'
├── address (TEXT)
├── city (TEXT)
├── pincode (TEXT)
├── credit_limit (NUMERIC)
├── outstanding_balance (NUMERIC)
└── created_at (TIMESTAMPTZ)
```

---

## Data Flow

### Creating a Draft
```
Frontend Form (CGST/SGST fields)
    ↓
collectSalData() - gathers all customer fields + items
    ↓
saveDraftOnly() - sends flat fields to API
    ↓
POST /api/drafts
    ↓
Backend creates row in drafts table with:
- All customer columns populated
- items JSONB array with cgst/sgst per item
- NO customer_id yet (nullable)
```

### Converting Draft to Invoice
```
Draft (with all customer details)
    ↓
draft_to_invoice()
    ↓
1. Create/Update customer in customers table
2. Create invoice with:
   - customer_id (reference)
   - All denormalized customer columns (copy from draft)
   - items array (copy from draft)
   - invoice_no (generated)
3. Delete draft
```

---

## Column Counts

| Table | OLD Columns | NEW Columns | Item Storage |
|-------|------------|------------|--------------|
| drafts | 8 | 8 + 17 customer + 1 items = 26 | JSONB array |
| invoices | 9 | 9 + 17 customer + 1 items + 1 invoice_no = 28 | JSONB array |
| draft_items | - | DROPPED | - |
| invoice_items | - | DROPPED | - |
| proforma_items | - | DROPPED | - |

---

## Example Data in JSONB

### Before (Separate Tables)
```
drafts row:
{
  id: "123e4567-e89b-12d3-a456",
  customer_id: "456f7890-f90c-23e4-b567",
  subtotal: 1000,
  total_gst: 180,
  ...
}

draft_items rows:
[
  {
    draft_id: "123e4567-e89b-12d3-a456",
    product_id: "789a1234-a12b-34c5-d678",
    qty: 10,
    gst: 9
  },
  {
    draft_id: "123e4567-e89b-12d3-a456",
    product_id: "890b2345-b23c-45d6-e789",
    qty: 5,
    gst: 5
  }
]
```

### After (JSONB)
```
drafts row:
{
  id: "123e4567-e89b-12d3-a456",
  customer_id: NULL (optional),
  type: "retailer",
  customer_name: "ABC Pharmacy",
  customer_phone: "9876543210",
  customer_gstin: "36AABCT1234H1Z0",
  customer_address: "123 Main St",
  customer_city: "Hyderabad",
  customer_state: "Telangana",
  subtotal: 1000,
  total_gst: 180,
  items: [
    {
      product_id: "789a1234-a12b-34c5-d678",
      qty: 10,
      cgst: 4.5,
      sgst: 4.5,
      sale_rate: 100
    },
    {
      product_id: "890b2345-b23c-45d6-e789",
      qty: 5,
      cgst: 2.5,
      sgst: 2.5,
      sale_rate: 50
    }
  ]
}
```

---

## Performance Considerations

### Indexes Added
```
drafts table:
- idx_drafts_phone (customer_phone) - for phone lookup
- idx_drafts_gstin (customer_gstin) - for GST lookup  
- idx_drafts_type (type) - for filtering by type

invoices table:
- idx_invoices_phone (customer_phone) - for customer invoices
- idx_invoices_gstin (customer_gstin) - for GST lookup
- idx_invoices_type (type) - for filtering
- idx_invoices_number (invoice_no) - for invoice lookup
```

These indexes speed up:
- Smart draft lookup by phone/GSTIN
- Filtering by customer type
- Finding invoices by customer

---

## Summary Command

To see all changes at once, run this in Supabase SQL Editor:

```sql
-- See all columns in drafts
SELECT column_name, data_type FROM information_schema.columns 
WHERE table_name = 'drafts' ORDER BY ordinal_position;

-- See all columns in invoices  
SELECT column_name, data_type FROM information_schema.columns 
WHERE table_name = 'invoices' ORDER BY ordinal_position;
```

After migration, drafts should have 26 columns and invoices should have 28 columns.
