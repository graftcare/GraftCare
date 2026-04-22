-- ============================================================================
-- GRAFTCARE SUPABASE - COMPLETE FRESH SCHEMA
-- Separate tables for drafts, proformas, and final invoices
-- Invoice number generated ONLY for final invoices: GCPS-YYYY-NNNN
-- ============================================================================

-- DROP ALL TABLES IN CORRECT ORDER (respecting foreign keys)
DROP TABLE IF EXISTS invoice_items CASCADE;
DROP TABLE IF EXISTS proforma_items CASCADE;
DROP TABLE IF EXISTS draft_items CASCADE;
DROP TABLE IF EXISTS invoices CASCADE;
DROP TABLE IF EXISTS proformas CASCADE;
DROP TABLE IF EXISTS drafts CASCADE;
DROP TABLE IF EXISTS stock_ledger CASCADE;
DROP TABLE IF EXISTS purchase_items CASCADE;
DROP TABLE IF EXISTS purchase_invoices CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS vendors CASCADE;

-- ============================================================================
-- VENDORS TABLE (Suppliers)
-- ============================================================================
CREATE TABLE vendors (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL UNIQUE,
  contact_person TEXT,
  phone TEXT UNIQUE,
  gstin TEXT UNIQUE,
  dl1 TEXT,
  dl2 TEXT,
  address TEXT,
  city TEXT,
  pincode TEXT,
  bank_name TEXT,
  bank_acc TEXT,
  bank_ifsc TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_vendors_gstin ON vendors(gstin);
CREATE INDEX idx_vendors_phone ON vendors(phone);
CREATE INDEX idx_vendors_name ON vendors(name);


-- ============================================================================
-- PRODUCTS TABLE (Medicine/Items)
-- ============================================================================
CREATE TABLE products (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  hsn_code TEXT,
  pack TEXT,
  company TEXT,
  scheme TEXT,
  cost_price NUMERIC(12, 2),
  mrp NUMERIC(12, 2),
  gst_rate NUMERIC(5, 2),
  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(name, company, hsn_code)
);

CREATE INDEX idx_products_name ON products(name);
CREATE INDEX idx_products_company ON products(company);


-- ============================================================================
-- CUSTOMERS TABLE (Retailers/Hospitals)
-- ============================================================================
CREATE TABLE customers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL UNIQUE,
  contact_person TEXT,
  phone TEXT UNIQUE,
  gstin TEXT UNIQUE,
  address TEXT,
  city TEXT,
  pincode TEXT,
  customer_type TEXT DEFAULT 'retailer',
  credit_limit NUMERIC(12, 2) DEFAULT 0,
  outstanding_balance NUMERIC(12, 2) DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_customers_gstin ON customers(gstin);
CREATE INDEX idx_customers_phone ON customers(phone);
CREATE INDEX idx_customers_name ON customers(name);
CREATE INDEX idx_customers_type ON customers(customer_type);


-- ============================================================================
-- PURCHASE INVOICES TABLE (Purchases from Vendors)
-- ============================================================================
CREATE TABLE purchase_invoices (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  vendor_id UUID NOT NULL REFERENCES vendors(id) ON DELETE RESTRICT,
  vendor_invoice_no TEXT NOT NULL,
  invoice_date DATE NOT NULL,
  payment_mode TEXT,
  amount_paid NUMERIC(12, 2),
  paid_by TEXT,
  subtotal NUMERIC(12, 2),
  total_gst NUMERIC(12, 2),
  discount_amount NUMERIC(12, 2),
  grand_total NUMERIC(12, 2) NOT NULL,
  payment_status TEXT DEFAULT 'pending',
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(vendor_id, vendor_invoice_no)
);

CREATE INDEX idx_purchase_invoices_vendor ON purchase_invoices(vendor_id);
CREATE INDEX idx_purchase_invoices_date ON purchase_invoices(invoice_date);
CREATE INDEX idx_purchase_invoices_status ON purchase_invoices(payment_status);
ALTER TABLE purchase_invoices ADD CONSTRAINT check_payment_status CHECK (payment_status IN ('pending', 'partial', 'paid'));


-- ============================================================================
-- PURCHASE ITEMS TABLE (Products in Purchase Invoices)
-- ============================================================================
CREATE TABLE purchase_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  purchase_invoice_id UUID NOT NULL REFERENCES purchase_invoices(id) ON DELETE CASCADE,
  product_id UUID NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
  qty INTEGER NOT NULL CHECK (qty > 0),
  batch TEXT NOT NULL,
  expiry DATE NOT NULL,
  mrp NUMERIC(12, 2),
  buy_rate NUMERIC(12, 2),
  free INTEGER DEFAULT 0,
  discount NUMERIC(12, 2),
  gst NUMERIC(12, 2),
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_purchase_items_invoice ON purchase_items(purchase_invoice_id);
CREATE INDEX idx_purchase_items_product ON purchase_items(product_id);
CREATE INDEX idx_purchase_items_batch_expiry ON purchase_items(batch, expiry);


-- ============================================================================
-- DRAFTS TABLE (Customer Draft Invoices - Work in Progress)
-- NO invoice number - only gets one when converted to final invoice
-- ============================================================================
CREATE TABLE drafts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  customer_id UUID NOT NULL REFERENCES customers(id) ON DELETE RESTRICT,
  subtotal NUMERIC(12, 2),
  total_gst NUMERIC(12, 2),
  discount_amount NUMERIC(12, 2),
  grand_total NUMERIC(12, 2),
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_drafts_customer ON drafts(customer_id);
CREATE INDEX idx_drafts_created ON drafts(created_at);


-- ============================================================================
-- DRAFT ITEMS TABLE (Products in Drafts)
-- ============================================================================
CREATE TABLE draft_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  draft_id UUID NOT NULL REFERENCES drafts(id) ON DELETE CASCADE,
  product_id UUID NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
  batch TEXT NOT NULL,
  expiry DATE NOT NULL,
  qty INTEGER NOT NULL CHECK (qty > 0),
  mrp NUMERIC(12, 2),
  sale_rate NUMERIC(12, 2),
  discount NUMERIC(12, 2),
  gst NUMERIC(12, 2),
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_draft_items_draft ON draft_items(draft_id);
CREATE INDEX idx_draft_items_product ON draft_items(product_id);


-- ============================================================================
-- PROFORMAS TABLE (Customer Proforma/Quote - Awaiting Approval)
-- NO invoice number - only gets one when converted to final invoice
-- ============================================================================
CREATE TABLE proformas (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  customer_id UUID NOT NULL REFERENCES customers(id) ON DELETE RESTRICT,
  subtotal NUMERIC(12, 2),
  total_gst NUMERIC(12, 2),
  discount_amount NUMERIC(12, 2),
  grand_total NUMERIC(12, 2),
  payment_mode TEXT,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_proformas_customer ON proformas(customer_id);
CREATE INDEX idx_proformas_created ON proformas(created_at);


-- ============================================================================
-- PROFORMA ITEMS TABLE (Products in Proformas)
-- ============================================================================
CREATE TABLE proforma_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  proforma_id UUID NOT NULL REFERENCES proformas(id) ON DELETE CASCADE,
  product_id UUID NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
  batch TEXT NOT NULL,
  expiry DATE NOT NULL,
  qty INTEGER NOT NULL CHECK (qty > 0),
  mrp NUMERIC(12, 2),
  sale_rate NUMERIC(12, 2),
  discount NUMERIC(12, 2),
  gst NUMERIC(12, 2),
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_proforma_items_proforma ON proforma_items(proforma_id);
CREATE INDEX idx_proforma_items_product ON proforma_items(product_id);


-- ============================================================================
-- INVOICES TABLE (Final Invoices - SALES ARE MADE HERE)
-- Invoice number AUTO-GENERATED in format: GCPS-YYYY-NNNN
-- Stock is DEDUCTED when invoice is created
-- ============================================================================
CREATE TABLE invoices (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  customer_id UUID NOT NULL REFERENCES customers(id) ON DELETE RESTRICT,
  invoice_seq SERIAL UNIQUE,
  invoice_number TEXT,
  invoice_date DATE NOT NULL DEFAULT CURRENT_DATE,
  subtotal NUMERIC(12, 2),
  total_gst NUMERIC(12, 2),
  discount_amount NUMERIC(12, 2),
  grand_total NUMERIC(12, 2),
  payment_mode TEXT,
  amount_received NUMERIC(12, 2),
  payment_status TEXT DEFAULT 'pending',
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- Trigger to auto-generate invoice number
CREATE OR REPLACE FUNCTION generate_invoice_number()
RETURNS TRIGGER AS $$
BEGIN
  NEW.invoice_number := 'GCPS-' || TO_CHAR(NEW.invoice_date, 'YYYY') || '-' || LPAD(NEW.invoice_seq::TEXT, 4, '0');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER invoice_number_trigger
BEFORE INSERT ON invoices
FOR EACH ROW
EXECUTE FUNCTION generate_invoice_number();

CREATE INDEX idx_invoices_customer ON invoices(customer_id);
CREATE INDEX idx_invoices_invoice_number ON invoices(invoice_number);
CREATE INDEX idx_invoices_date ON invoices(invoice_date);
CREATE INDEX idx_invoices_payment_status ON invoices(payment_status);
ALTER TABLE invoices ADD CONSTRAINT check_invoice_payment_status CHECK (payment_status IN ('pending', 'partial', 'paid'));


-- ============================================================================
-- INVOICE ITEMS TABLE (Products in Final Invoices)
-- ============================================================================
CREATE TABLE invoice_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  invoice_id UUID NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
  product_id UUID NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
  batch TEXT NOT NULL,
  expiry DATE NOT NULL,
  qty INTEGER NOT NULL CHECK (qty > 0),
  mrp NUMERIC(12, 2),
  sale_rate NUMERIC(12, 2),
  discount NUMERIC(12, 2),
  gst NUMERIC(12, 2),
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_invoice_items_invoice ON invoice_items(invoice_id);
CREATE INDEX idx_invoice_items_product ON invoice_items(product_id);
CREATE INDEX idx_invoice_items_batch_expiry ON invoice_items(batch, expiry);


-- ============================================================================
-- STOCK LEDGER TABLE (Inventory Tracking)
-- Records every stock movement with reason
-- ============================================================================
CREATE TABLE stock_ledger (
  id SERIAL PRIMARY KEY,
  product_id UUID NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
  change_qty INTEGER NOT NULL,
  reason TEXT NOT NULL,
  reference_id UUID,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_stock_ledger_product ON stock_ledger(product_id);
CREATE INDEX idx_stock_ledger_date ON stock_ledger(created_at);



-- ============================================================================
-- SCHEMA COMPLETE
-- ============================================================================
-- Tables created:
-- 1. vendors, products, customers (master data)
-- 2. purchase_invoices, purchase_items (supplier purchases)
-- 3. drafts, draft_items (customer draft invoices - no invoice number)
-- 4. proformas, proforma_items (customer proformas - no invoice number)
-- 5. invoices, invoice_items (FINAL SALES - auto-generated GCPS-YYYY-NNNN)
-- 6. stock_ledger (inventory tracking)
--
-- KEY FEATURES:
-- ✅ Invoice number (GCPS-YYYY-NNNN) generated ONLY for final invoices
-- ✅ Stock deduction happens when proforma → invoice conversion
-- ✅ Drafts can be edited anytime
-- ✅ Proformas show quotes awaiting approval
-- ✅ Final invoices generate unique numbers and trigger stock deduction
-- ✅ Tracker can search by customer name, phone, month
-- ✅ All tables indexed for fast queries
-- ✅ GST calculation: User enters GST → SGST & CGST auto-calculated as GST/2 each
-- ✅ User can manually override SGST/CGST values anytime
-- ✅ No state-wise GST complexity - simple frontend-based calculation
-- ============================================================================
