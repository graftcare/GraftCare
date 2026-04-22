-- ============================================================================
-- CLEAR ALL DATA FROM ALL TABLES (Keep schema, reset sequences)
-- ============================================================================
-- Execute these in order to avoid foreign key constraint violations

-- Delete from dependent tables first (those with foreign keys)
DELETE FROM sales_items;
DELETE FROM purchase_items;
DELETE FROM stock_ledger;

-- Delete from main tables (those with foreign keys to others)
DELETE FROM sales;
DELETE FROM purchase_invoices;

-- Delete from reference tables (vendors, products, customers)
DELETE FROM customers;
DELETE FROM products;
DELETE FROM vendors;

-- ============================================================================
-- RESET AUTO-INCREMENT SEQUENCES
-- ============================================================================
-- Reset the invoice number sequences back to 1

-- For sales invoice number
ALTER SEQUENCE sales_invoice_seq RESTART WITH 1;

-- For purchase invoice number (if exists)
-- ALTER SEQUENCE purchase_invoices_invoice_seq RESTART WITH 1;

-- ============================================================================
-- VERIFY ALL TABLES ARE EMPTY
-- ============================================================================
SELECT 'vendors' as table_name, COUNT(*) as record_count FROM vendors
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'customers', COUNT(*) FROM customers
UNION ALL
SELECT 'purchase_invoices', COUNT(*) FROM purchase_invoices
UNION ALL
SELECT 'purchase_items', COUNT(*) FROM purchase_items
UNION ALL
SELECT 'sales', COUNT(*) FROM sales
UNION ALL
SELECT 'sales_items', COUNT(*) FROM sales_items
UNION ALL
SELECT 'stock_ledger', COUNT(*) FROM stock_ledger;
