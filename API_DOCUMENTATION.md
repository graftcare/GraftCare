# Graftcare API Documentation

## Overview

Complete RESTful API for pharmaceutical inventory management system built with FastAPI and Supabase.

**Base URL:** `http://localhost:8000`

---

## Authentication

Currently, the API is open (no authentication required). For production, add API key authentication.

---

## Response Format

All endpoints return JSON responses with appropriate HTTP status codes.

### Success Response
```json
{
  "id": "uuid",
  "message": "Operation successful"
}
```

### Error Response
```json
{
  "detail": "Error message"
}
```

---

## Endpoints

### Health Check

#### GET `/health`
Check API status
```bash
curl http://localhost:8000/health
```

**Response:** 200 OK
```json
{
  "status": "healthy",
  "timestamp": "2026-04-22T10:30:00"
}
```

---

## Vendors (Master Data)

### GET `/api/vendors`
Get all vendors
```bash
curl http://localhost:8000/api/vendors
```

**Response:** 200 OK
```json
[
  {
    "id": "uuid",
    "name": "Gaudev and Co",
    "contact_person": "John",
    "phone": "9876543210",
    "gstin": "27AAPFU1234H1Z0",
    "address": "123 Main St",
    "city": "Mumbai",
    "pincode": "400001",
    "bank_name": "HDFC",
    "bank_acc": "1234567890",
    "bank_ifsc": "HDFC0001234",
    "created_at": "2026-04-22T10:00:00"
  }
]
```

### GET `/api/vendors/{vendor_id}`
Get vendor by ID
```bash
curl http://localhost:8000/api/vendors/uuid
```

### POST `/api/vendors`
Create new vendor
```bash
curl -X POST http://localhost:8000/api/vendors \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Gaudev and Co",
    "phone": "9876543210",
    "gstin": "27AAPFU1234H1Z0",
    "contact_person": "John",
    "address": "123 Main St",
    "city": "Mumbai",
    "pincode": "400001"
  }'
```

**Response:** 200 OK
```json
{
  "id": "uuid",
  "message": "Vendor created successfully"
}
```

### PUT `/api/vendors/{vendor_id}`
Update vendor
```bash
curl -X PUT http://localhost:8000/api/vendors/uuid \
  -H "Content-Type: application/json" \
  -d '{"phone": "9999999999"}'
```

### DELETE `/api/vendors/{vendor_id}`
Delete vendor
```bash
curl -X DELETE http://localhost:8000/api/vendors/uuid
```

---

## Products (Master Data)

### GET `/api/products`
Get all products
```bash
curl http://localhost:8000/api/products
```

### POST `/api/products`
Create new product
```bash
curl -X POST http://localhost:8000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dolo 650",
    "hsn_code": "300590",
    "pack": "10",
    "company": "Cipla",
    "cost_price": 10.0,
    "mrp": 30.0,
    "gst_rate": 18.0
  }'
```

### PUT `/api/products/{product_id}`
Update product

### DELETE `/api/products/{product_id}`
Delete product

---

## Customers (Master Data)

### GET `/api/customers`
Get all customers

### POST `/api/customers`
Create new customer
```bash
curl -X POST http://localhost:8000/api/customers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Apollo Hospital",
    "phone": "9876543210",
    "gstin": "27AAPFU1234H1Z0",
    "contact_person": "Manager",
    "address": "456 Hospital Rd",
    "city": "Mumbai",
    "pincode": "400001",
    "customer_type": "hospital",
    "credit_limit": 100000.0
  }'
```

### PUT `/api/customers/{customer_id}`
Update customer

### DELETE `/api/customers/{customer_id}`
Delete customer

---

## Purchase Invoices (Stock IN from Vendors)

### GET `/api/purchase-invoices`
Get all purchase invoices with items

### GET `/api/purchase-invoices/{invoice_id}`
Get specific purchase invoice

### POST `/api/purchase-invoices`
Create purchase invoice (auto-updates stock)
```bash
curl -X POST http://localhost:8000/api/purchase-invoices \
  -H "Content-Type: application/json" \
  -d '{
    "vendor_id": "uuid",
    "vendor_invoice_no": "INV-2026-001",
    "invoice_date": "2026-04-22",
    "subtotal": 1000.0,
    "total_gst": 180.0,
    "grand_total": 1180.0,
    "payment_mode": "bank_transfer",
    "payment_status": "pending",
    "items": [
      {
        "product_id": "uuid",
        "qty": 100,
        "batch": "BATCH-123",
        "expiry": "2027-04-22",
        "buy_rate": 10.0,
        "mrp": 30.0,
        "gst": 18.0
      }
    ]
  }'
```

**Effect:** ✅ **Stock INCREASES** by qty for each item

### PUT `/api/purchase-invoices/{invoice_id}`
Update purchase invoice

### DELETE `/api/purchase-invoices/{invoice_id}`
Delete purchase invoice (reverses stock)

**Effect:** ✅ **Stock DECREASES** by qty (reversal entry)

---

## Drafts (Work in Progress)

### GET `/api/drafts`
Get all draft invoices with items

### GET `/api/drafts/{draft_id}`
Get specific draft

### POST `/api/drafts`
Create draft invoice (no stock change)
```bash
curl -X POST http://localhost:8000/api/drafts \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "uuid",
    "subtotal": 5000.0,
    "total_gst": 900.0,
    "grand_total": 5900.0,
    "items": [
      {
        "product_id": "uuid",
        "qty": 50,
        "batch": "BATCH-456",
        "expiry": "2027-05-22",
        "sale_rate": 100.0,
        "mrp": 120.0,
        "gst": 18.0
      }
    ]
  }'
```

**Effect:** ❌ **NO stock change** - still editing

### PUT `/api/drafts/{draft_id}`
Update draft (can edit anytime)

### DELETE `/api/drafts/{draft_id}`
Delete draft

### POST `/api/drafts/{draft_id}/to-proforma`
Convert draft to proforma
```bash
curl -X POST http://localhost:8000/api/drafts/uuid/to-proforma
```

**Effect:** ❌ **NO stock change** - awaiting approval

---

## Proformas (Quotes Sent to Customer)

### GET `/api/proformas`
Get all proformas

### GET `/api/proformas/{proforma_id}`
Get specific proforma

### POST `/api/proformas`
Create proforma directly

### PUT `/api/proformas/{proforma_id}`
Update proforma

### DELETE `/api/proformas/{proforma_id}`
Delete proforma

### POST `/api/proformas/{proforma_id}/finalize`
Convert proforma to final invoice (creates GCPS-YYYY-NNNN number and deducts stock)
```bash
curl -X POST http://localhost:8000/api/proformas/uuid/finalize
```

**Response:** 200 OK
```json
{
  "id": "invoice_uuid",
  "invoice_number": "GCPS-2026-0001",
  "message": "Proforma finalized to invoice successfully"
}
```

**Effect:** ✅ **Stock DECREASES** by qty for each item, invoice number auto-generated

---

## Invoices (Final Sales)

### GET `/api/invoices`
Get all final invoices

### GET `/api/invoices/{invoice_id}`
Get specific invoice

### GET `/api/customers/{customer_id}/invoices`
Get all invoices for specific customer

### PUT `/api/invoices/{invoice_id}`
Update invoice (payment status, amount received)
```bash
curl -X PUT http://localhost:8000/api/invoices/uuid \
  -H "Content-Type: application/json" \
  -d '{
    "payment_mode": "cash",
    "amount_received": 5900.0,
    "payment_status": "paid"
  }'
```

### DELETE `/api/invoices/{invoice_id}`
Delete invoice (reverses stock)

**Effect:** ✅ **Stock INCREASES** by qty (reversal/refund)

---

## Stock Management

### GET `/api/stock`
Get all stock ledger entries (shows all movements)

### GET `/api/stock/{product_id}`
Get current stock for product
```bash
curl http://localhost:8000/api/stock/uuid
```

**Response:** 200 OK
```json
{
  "product_id": "uuid",
  "product_name": "Dolo 650",
  "current_stock": 250
}
```

**Note:** Current stock = SUM of all `change_qty` in stock_ledger for that product

---

## Dashboard

### GET `/api/dashboard`
Get dashboard statistics
```bash
curl http://localhost:8000/api/dashboard
```

**Response:** 200 OK
```json
{
  "vendors": 15,
  "products": 250,
  "customers": 45,
  "total_revenue": 500000.0,
  "total_sales": 120
}
```

---

## Complete Workflow Example

### 1. Create Vendor
```bash
POST /api/vendors
```

### 2. Create Products
```bash
POST /api/products
```

### 3. Create Purchase Invoice (Stock increases)
```bash
POST /api/purchase-invoices
# Stock Ledger: +100 qty for product (reason: "purchase")
```

### 4. Create Customer
```bash
POST /api/customers
```

### 5. Create Draft Invoice
```bash
POST /api/drafts
# No stock change
```

### 6. Convert Draft to Proforma
```bash
POST /api/drafts/{id}/to-proforma
# No stock change
```

### 7. Finalize Proforma to Invoice
```bash
POST /api/proformas/{id}/finalize
# Stock Ledger: -50 qty for product (reason: "sale")
# Invoice Number: GCPS-2026-0001 (auto-generated)
```

### 8. Update Invoice Payment
```bash
PUT /api/invoices/{id}
```

---

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Success |
| 400 | Bad Request - Validation error |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error |

---

## Key Features

✅ **Automatic Invoice Number Generation:** GCPS-YYYY-NNNN format only for final invoices
✅ **Stock Management:** Real-time tracking with ledger
✅ **Multi-Stage Sales:** Draft → Proforma → Invoice workflow
✅ **Batch & Expiry Tracking:** Per-item batch and expiry dates
✅ **Complete Audit Trail:** Stock ledger records all movements with reasons
✅ **Error Handling:** Proper validation and error responses
✅ **No State-Wise Complexity:** Simple GST/2 calculation in frontend

---

## Running the API

```bash
# Install dependencies
pip install fastapi uvicorn supabase python-dotenv

# Set environment variables in .env
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_KEY=your_service_key

# Run server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

**Last Updated:** 2026-04-22
**Version:** 1.0.0
**Status:** Production Ready
