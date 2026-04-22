# Database Tables Schema

## 1. VENDORS
| Column | Type | Constraints |
|--------|------|-----------|
| id | UUID | PK, DEFAULT: gen_random_uuid() |
| name | TEXT | NOT NULL |
| contact_person | TEXT | |
| phone | TEXT | UNIQUE |
| gstin | TEXT | UNIQUE |
| dl1 | TEXT | |
| dl2 | TEXT | |
| address | TEXT | |
| city | TEXT | |
| pincode | TEXT | |
| bank_name | TEXT | |
| bank_acc | TEXT | |
| bank_ifsc | TEXT | |
| created_at | TIMESTAMPTZ | DEFAULT: now() |

---

## 2. PRODUCTS
| Column | Type | Constraints |
|--------|------|-----------|
| id | UUID | PK, DEFAULT: gen_random_uuid() |
| name | TEXT | NOT NULL |
| hsn_code | TEXT | |
| pack | TEXT | |
| company | TEXT | |
| scheme | TEXT | |
| cost_price | NUMERIC(12,2) | |
| mrp | NUMERIC(12,2) | |
| gst_rate | NUMERIC(5,2) | |
| created_at | TIMESTAMPTZ | DEFAULT: now() |
| **UNIQUE** | | (name, company, hsn_code) |

---

## 3. PURCHASE_INVOICES
| Column | Type | Constraints |
|--------|------|-----------|
| id | UUID | PK, DEFAULT: gen_random_uuid() |
| vendor_id | UUID | FK → vendors.id, NOT NULL, ON DELETE RESTRICT |
| vendor_invoice_no | TEXT | NOT NULL |
| invoice_date | DATE | NOT NULL |
| payment_mode | TEXT | |
| amount_paid | NUMERIC(12,2) | |
| paid_by | TEXT | |
| subtotal | NUMERIC(12,2) | |
| total_gst | NUMERIC(12,2) | |
| discount_amount | NUMERIC(12,2) | |
| grand_total | NUMERIC(12,2) | NOT NULL |
| payment_status | TEXT | DEFAULT: 'pending' |
| notes | TEXT | |
| created_at | TIMESTAMPTZ | DEFAULT: now() |
| **UNIQUE** | | (vendor_id, vendor_invoice_no) |

---

## 4. PURCHASE_ITEMS
| Column | Type | Constraints |
|--------|------|-----------|
| id | UUID | PK, DEFAULT: gen_random_uuid() |
| purchase_invoice_id | UUID | FK → purchase_invoices.id, NOT NULL, ON DELETE CASCADE |
| product_id | UUID | FK → products.id, NOT NULL, ON DELETE RESTRICT |
| qty | INTEGER | NOT NULL |
| batch | TEXT | NOT NULL |
| expiry | DATE | NOT NULL |
| mrp | NUMERIC(12,2) | |
| buy_rate | NUMERIC(12,2) | |
| free | INTEGER | DEFAULT: 0 |
| discount | NUMERIC(12,2) | |
| gst | NUMERIC(12,2) | |
| created_at | TIMESTAMPTZ | DEFAULT: now() |

---

## 5. CUSTOMERS
| Column | Type | Constraints |
|--------|------|-----------|
| id | UUID | PK, DEFAULT: gen_random_uuid() |
| name | TEXT | NOT NULL |
| contact_person | TEXT | |
| phone | TEXT | UNIQUE |
| gstin | TEXT | UNIQUE |
| address | TEXT | |
| city | TEXT | |
| pincode | TEXT | |
| credit_limit | NUMERIC(12,2) | DEFAULT: 0 |
| outstanding_balance | NUMERIC(12,2) | DEFAULT: 0 |
| created_at | TIMESTAMPTZ | DEFAULT: now() |

---

## 6. SALES
| Column | Type | Constraints |
|--------|------|-----------|
| id | UUID | PK, DEFAULT: gen_random_uuid() |
| customer_id | UUID | FK → customers.id, NOT NULL, ON DELETE RESTRICT |
| status | TEXT | DEFAULT: 'draft' |
| invoice_date | DATE | |
| subtotal | NUMERIC(12,2) | |
| total_gst | NUMERIC(12,2) | |
| discount_amount | NUMERIC(12,2) | |
| grand_total | NUMERIC(12,2) | |
| payment_mode | TEXT | |
| amount_received | NUMERIC(12,2) | |
| notes | TEXT | |
| created_at | TIMESTAMPTZ | DEFAULT: now() |
| updated_at | TIMESTAMPTZ | DEFAULT: now() |

---

## 7. SALES_ITEMS
| Column | Type | Constraints |
|--------|------|-----------|
| id | UUID | PK, DEFAULT: gen_random_uuid() |
| sale_id | UUID | FK → sales.id, NOT NULL, ON DELETE CASCADE |
| product_id | UUID | FK → products.id, NOT NULL, ON DELETE RESTRICT |
| batch | TEXT | NOT NULL |
| expiry | DATE | NOT NULL |
| qty | INTEGER | NOT NULL |
| mrp | NUMERIC(12,2) | |
| sale_rate | NUMERIC(12,2) | |
| discount | NUMERIC(12,2) | |
| gst | NUMERIC(12,2) | |
| created_at | TIMESTAMPTZ | DEFAULT: now() |

---

## 8. STOCK_LEDGER
| Column | Type | Constraints |
|--------|------|-----------|
| id | SERIAL | PK |
| product_id | UUID | FK → products.id, NOT NULL, ON DELETE RESTRICT |
| change_qty | INTEGER | NOT NULL |
| reason | TEXT | NOT NULL |
| reference_id | UUID | |
| notes | TEXT | |
| created_at | TIMESTAMPTZ | DEFAULT: now() |
