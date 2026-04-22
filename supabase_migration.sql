-- ============================================================================
-- GRAFTCARE SUPABASE - MIGRATION TO DENORMALIZED SCHEMA
-- Convert to flat individual customer columns in drafts/invoices
-- Store items as JSONB array instead of separate tables
-- ============================================================================

-- Step 1: Drop old item tables (in correct order due to foreign keys)
DROP TABLE IF EXISTS invoice_items CASCADE;
DROP TABLE IF EXISTS proforma_items CASCADE;
DROP TABLE IF EXISTS draft_items CASCADE;

-- Step 2: Update drafts table - make customer_id nullable and add individual columns
ALTER TABLE drafts ALTER COLUMN customer_id DROP NOT NULL;

-- Add type and counter columns
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS "type" VARCHAR(20) DEFAULT 'patient';
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS draft_counter INTEGER DEFAULT 1;

-- Add common customer columns
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_name VARCHAR(255);
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_phone VARCHAR(20);
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_address TEXT;
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_city VARCHAR(100);
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_pincode VARCHAR(10);
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_state VARCHAR(100);
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_door_number VARCHAR(100);

-- Add retailer-specific columns
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_gstin VARCHAR(50);
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_dl1 VARCHAR(100);
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_dl2 VARCHAR(100);

-- Add patient-specific columns
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_age VARCHAR(10);
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_gender VARCHAR(20);
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_doctor_name VARCHAR(255);
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_hospital_name VARCHAR(255);
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_doctor_phone VARCHAR(20);
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_is_member BOOLEAN DEFAULT FALSE;
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS customer_member_id VARCHAR(100);

-- Add items as JSONB array
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS items JSONB DEFAULT '[]'::jsonb;

-- Step 3: Update invoices table - add all same columns as drafts
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS "type" VARCHAR(20) DEFAULT 'patient';
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS invoice_no VARCHAR(50);

-- Add common customer columns
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_name VARCHAR(255);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_phone VARCHAR(20);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_address TEXT;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_city VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_pincode VARCHAR(10);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_state VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_door_number VARCHAR(100);

-- Add retailer-specific columns
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_gstin VARCHAR(50);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_dl1 VARCHAR(100);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_dl2 VARCHAR(100);

-- Add patient-specific columns
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_age VARCHAR(10);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_gender VARCHAR(20);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_doctor_name VARCHAR(255);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_hospital_name VARCHAR(255);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_doctor_phone VARCHAR(20);
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_is_member BOOLEAN DEFAULT FALSE;
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_member_id VARCHAR(100);

-- Add items as JSONB array
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS items JSONB DEFAULT '[]'::jsonb;

-- Step 4: Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_drafts_phone ON drafts(customer_phone);
CREATE INDEX IF NOT EXISTS idx_drafts_gstin ON drafts(customer_gstin);
CREATE INDEX IF NOT EXISTS idx_drafts_type ON drafts("type");
CREATE INDEX IF NOT EXISTS idx_invoices_phone ON invoices(customer_phone);
CREATE INDEX IF NOT EXISTS idx_invoices_gstin ON invoices(customer_gstin);
CREATE INDEX IF NOT EXISTS idx_invoices_type ON invoices("type");
CREATE INDEX IF NOT EXISTS idx_invoices_number ON invoices(invoice_no);
