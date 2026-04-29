"""
Complete Supabase Database Client
All database operations for Graftcare system
"""

import os
from pathlib import Path
from supabase import create_client, Client
from dotenv import load_dotenv

# Load .env from parent directory (project root)
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Initialize Supabase client - load from .env file
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL:
    print("CRITICAL ERROR: SUPABASE_URL is not set in environment variables!")
if not SUPABASE_SERVICE_KEY:
    print("CRITICAL ERROR: SUPABASE_SERVICE_KEY is not set in environment variables!")

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    raise Exception("Missing SUPABASE credentials. Please set SUPABASE_URL and SUPABASE_SERVICE_KEY in the Render Environment settings.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# ============================================================================
# VENDORS - Database operations
# ============================================================================

async def get_vendors():
    """Get all vendors"""
    try:
        response = supabase.table("vendors").select("*").order("name").execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching vendors: {e}")
        return []

async def create_vendor(vendor_data):
    """Create new vendor"""
    try:
        response = supabase.table("vendors").insert(vendor_data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error creating vendor: {e}")
        raise

async def update_vendor(vendor_id, vendor_data):
    """Update vendor"""
    try:
        response = supabase.table("vendors").update(vendor_data).eq("id", vendor_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error updating vendor: {e}")
        raise

async def delete_vendor(vendor_id):
    """Delete vendor"""
    try:
        response = supabase.table("vendors").delete().eq("id", vendor_id).execute()
        return True
    except Exception as e:
        print(f"Error deleting vendor: {e}")
        raise

async def get_vendor_by_gstin(gstin):
    """Get vendor by GSTIN"""
    try:
        response = supabase.table("vendors").select("*").eq("gstin", gstin).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error fetching vendor by GSTIN: {e}")
        return None

async def get_vendor_by_phone(phone):
    """Get vendor by phone"""
    try:
        response = supabase.table("vendors").select("*").eq("phone", phone).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error fetching vendor by phone: {e}")
        return None

async def get_vendor_by_id(vendor_id):
    """Get vendor by ID"""
    try:
        response = supabase.table("vendors").select("*").eq("id", vendor_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error fetching vendor by ID: {e}")
        return None

# ============================================================================
# PRODUCTS - Database operations
# ============================================================================

async def get_products():
    """Get all products"""
    try:
        response = supabase.table("products").select("*").order("name").execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching products: {e}")
        return []

async def create_product(product_data):
    """Create new product"""
    try:
        response = supabase.table("products").insert(product_data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error creating product: {e}")
        raise

async def update_product(product_id, product_data):
    """Update product"""
    try:
        response = supabase.table("products").update(product_data).eq("id", product_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error updating product: {e}")
        raise

async def delete_product(product_id):
    """Delete product"""
    try:
        response = supabase.table("products").delete().eq("id", product_id).execute()
        return True
    except Exception as e:
        print(f"Error deleting product: {e}")
        raise

async def get_product_by_id(product_id):
    """Get product by ID"""
    try:
        response = supabase.table("products").select("*").eq("id", product_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error fetching product by ID: {e}")
        return None

# ============================================================================
# CUSTOMERS - Database operations
# ============================================================================

async def get_customers():
    """Get all customers"""
    try:
        response = supabase.table("customers").select("*").order("name").execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching customers: {e}")
        return []

async def create_customer(customer_data):
    """Create new customer"""
    try:
        response = supabase.table("customers").insert(customer_data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error creating customer: {e}")
        raise

async def update_customer(customer_id, customer_data):
    """Update customer"""
    try:
        response = supabase.table("customers").update(customer_data).eq("id", customer_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error updating customer: {e}")
        raise

async def delete_customer(customer_id):
    """Delete customer"""
    try:
        response = supabase.table("customers").delete().eq("id", customer_id).execute()
        return True
    except Exception as e:
        print(f"Error deleting customer: {e}")
        raise

async def get_customer_by_id(customer_id):
    """Get customer by ID"""
    try:
        response = supabase.table("customers").select("*").eq("id", customer_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error fetching customer by ID: {e}")
        return None

async def get_customer_by_phone(phone):
    """Get customer by phone"""
    try:
        response = supabase.table("customers").select("*").eq("phone", phone).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error fetching customer by phone: {e}")
        return None

async def get_customer_by_gstin(gstin):
    """Get customer by GSTIN"""
    try:
        response = supabase.table("customers").select("*").eq("gstin", gstin).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error fetching customer by GSTIN: {e}")
        return None

# ============================================================================
# PURCHASE INVOICES - Database operations
# ============================================================================

async def get_purchase_items_by_invoice(invoice_id):
    """Get items from purchase_items table with product details"""
    try:
        response = supabase.table("purchase_items").select("*,product_id(name)").eq("purchase_invoice_id", invoice_id).execute()
        items = response.data if response.data else []
        # Flatten the product name from nested object
        for item in items:
            if isinstance(item.get('product_id'), dict) and 'name' in item['product_id']:
                item['name'] = item['product_id']['name']
        return items
    except Exception as e:
        print(f"Error fetching purchase items: {e}")
        return []

async def enrich_items_with_product_names(items):
    """Enrich items with product names by fetching from products table"""
    try:
        for item in items:
            if not item.get('name'):
                product_id = item.get('product_id')
                if isinstance(product_id, str):
                    product = await get_product_by_id(product_id)
                    if product:
                        item['name'] = product.get('name', product_id)
                elif isinstance(product_id, dict) and 'name' in product_id:
                    item['name'] = product_id['name']
        return items
    except Exception as e:
        print(f"Error enriching items with product names: {e}")
        return items

async def get_purchase_invoices():
    """Get all purchase invoices - items will be fetched separately by API endpoint"""
    try:
        response = supabase.table("purchase_invoices").select("*").order("invoice_date", desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching purchase invoices: {e}")
        return []

async def get_purchase_invoice_by_id(invoice_id):
    """Get purchase invoice by ID with items (from JSONB or purchase_items table)"""
    try:
        response = supabase.table("purchase_invoices").select("*").eq("id", invoice_id).execute()
        if response.data:
            inv = response.data[0]
            # If items JSONB column is empty, fetch from purchase_items table
            if not inv.get('items'):
                items_from_table = await get_purchase_items_by_invoice(invoice_id)
                inv['items'] = items_from_table if items_from_table else []
            else:
                # Enrich JSONB items with product names
                inv['items'] = await enrich_items_with_product_names(inv['items'])
            return inv
        return None
    except Exception as e:
        print(f"Error fetching purchase invoice: {e}")
        return None

async def get_purchase_invoices_by_vendor(vendor_id):
    """Get all purchase invoices for a specific vendor with items (from JSONB or purchase_items table)"""
    try:
        response = supabase.table("purchase_invoices").select("*").eq("vendor_id", vendor_id).order("invoice_date", desc=True).execute()
        result = []
        if response.data:
            for inv in response.data:
                # If items JSONB column is empty, fetch from purchase_items table
                if not inv.get('items'):
                    items_from_table = await get_purchase_items_by_invoice(inv['id'])
                    inv['items'] = items_from_table if items_from_table else []
                else:
                    # Enrich JSONB items with product names
                    inv['items'] = await enrich_items_with_product_names(inv['items'])
                result.append(inv)
        return result
    except Exception as e:
        print(f"Error fetching vendor invoices: {e}")
        return []

async def create_purchase_invoice(invoice_data):
    """Create purchase invoice"""
    try:
        response = supabase.table("purchase_invoices").insert(invoice_data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error creating purchase invoice: {e}")
        raise

async def update_purchase_invoice(invoice_id, invoice_data):
    """Update purchase invoice"""
    try:
        response = supabase.table("purchase_invoices").update(invoice_data).eq("id", invoice_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error updating purchase invoice: {e}")
        raise

async def delete_purchase_invoice(invoice_id):
    """Delete purchase invoice"""
    try:
        response = supabase.table("purchase_invoices").delete().eq("id", invoice_id).execute()
        return True
    except Exception as e:
        print(f"Error deleting purchase invoice: {e}")
        raise

# ============================================================================
# PURCHASE ITEMS - Database operations
# ============================================================================

async def get_purchase_items(invoice_id):
    """Get items for purchase invoice with product details"""
    try:
        response = supabase.table("purchase_items").select("*,product_id(name)").eq("purchase_invoice_id", invoice_id).execute()
        items = response.data if response.data else []
        # Flatten the product name from nested object
        for item in items:
            if isinstance(item.get('product_id'), dict) and 'name' in item['product_id']:
                item['name'] = item['product_id']['name']
        return items
    except Exception as e:
        print(f"Error fetching purchase items: {e}")
        return []

async def create_purchase_items(items_data):
    """Create purchase items"""
    try:
        response = supabase.table("purchase_items").insert(items_data).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error creating purchase items: {e}")
        raise

async def delete_purchase_items(invoice_id):
    """Delete all items for purchase invoice"""
    try:
        response = supabase.table("purchase_items").delete().eq("purchase_invoice_id", invoice_id).execute()
        return True
    except Exception as e:
        print(f"Error deleting purchase items: {e}")
        raise

async def get_purchase_items_by_product(product_id):
    """Get all purchase items for a product"""
    try:
        response = supabase.table("purchase_items").select("*").eq("product_id", product_id).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching purchase items by product: {e}")
        return []

async def get_latest_purchase_item_for_product(product_id):
    """Get the most recent purchase item for a product (for batch/expiry)"""
    try:
        response = supabase.table("purchase_items").select("batch,expiry,created_at").eq("product_id", product_id).order("created_at", desc=True).limit(1).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error fetching latest purchase item: {e}")
        return None

async def get_invoice_items_by_product(product_id):
    """Get all invoice items (sold) for a product"""
    try:
        response = supabase.table("invoice_items").select("*").eq("product_id", product_id).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching invoice items by product: {e}")
        return []

# ============================================================================
# DRAFTS - Database operations
# ============================================================================

async def get_drafts():
    """Get all draft invoices"""
    try:
        response = supabase.table("drafts").select("*").order("created_at", desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching drafts: {e}")
        return []

async def get_draft_by_id(draft_id):
    """Get draft by ID"""
    try:
        response = supabase.table("drafts").select("*").eq("id", draft_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error fetching draft: {e}")
        return None

async def create_draft(draft_data):
    """Create draft invoice"""
    try:
        response = supabase.table("drafts").insert(draft_data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error creating draft: {e}")
        raise

async def update_draft(draft_id, draft_data):
    """Update draft invoice"""
    try:
        response = supabase.table("drafts").update(draft_data).eq("id", draft_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error updating draft: {e}")
        raise

async def delete_draft(draft_id):
    """Delete draft invoice"""
    try:
        response = supabase.table("drafts").delete().eq("id", draft_id).execute()
        return True
    except Exception as e:
        print(f"Error deleting draft: {e}")
        raise

async def lookup_draft_by_phone(phone: str, draft_type: str):
    """Look up draft by customer phone and type"""
    try:
        response = supabase.table("drafts").select("*").eq("customer_phone", phone).eq("type", draft_type).order("created_at", desc=True).limit(1).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error looking up draft by phone: {e}")
        return None

async def lookup_draft_by_gstin(gstin: str):
    """Look up draft by GSTIN (retailer only)"""
    try:
        response = supabase.table("drafts").select("*").eq("customer_gstin", gstin).eq("type", "retailer").order("created_at", desc=True).limit(1).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error looking up draft by GSTIN: {e}")
        return None

async def count_drafts_by_phone(phone: str):
    """Count total drafts for a customer by phone"""
    try:
        response = supabase.table("drafts").select("id", count="exact").eq("customer_phone", phone).execute()
        return response.count or 0
    except Exception as e:
        print(f"Error counting drafts by phone: {e}")
        return 0

# ============================================================================
# DRAFT ITEMS - Database operations
# ============================================================================

async def get_draft_items(draft_id):
    """Get items for draft invoice"""
    try:
        response = supabase.table("draft_items").select("*").eq("draft_id", draft_id).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching draft items: {e}")
        return []

async def create_draft_items(items_data):
    """Create draft items"""
    try:
        response = supabase.table("draft_items").insert(items_data).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error creating draft items: {e}")
        raise

async def delete_draft_items(draft_id):
    """Delete all items for draft"""
    try:
        response = supabase.table("draft_items").delete().eq("draft_id", draft_id).execute()
        return True
    except Exception as e:
        print(f"Error deleting draft items: {e}")
        raise

# ============================================================================
# PROFORMAS - Database operations
# ============================================================================

async def get_proformas():
    """Get all proforma invoices"""
    try:
        response = supabase.table("proformas").select("*").order("created_at", desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching proformas: {e}")
        return []

async def get_proforma_by_id(proforma_id):
    """Get proforma by ID"""
    try:
        response = supabase.table("proformas").select("*").eq("id", proforma_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error fetching proforma: {e}")
        return None

async def create_proforma(proforma_data):
    """Create proforma invoice"""
    try:
        response = supabase.table("proformas").insert(proforma_data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error creating proforma: {e}")
        raise

async def update_proforma(proforma_id, proforma_data):
    """Update proforma invoice"""
    try:
        response = supabase.table("proformas").update(proforma_data).eq("id", proforma_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error updating proforma: {e}")
        raise

async def delete_proforma(proforma_id):
    """Delete proforma invoice"""
    try:
        response = supabase.table("proformas").delete().eq("id", proforma_id).execute()
        return True
    except Exception as e:
        print(f"Error deleting proforma: {e}")
        raise

# ============================================================================
# PROFORMA ITEMS - Database operations
# ============================================================================

async def get_proforma_items(proforma_id):
    """Get items for proforma invoice"""
    try:
        response = supabase.table("proforma_items").select("*").eq("proforma_id", proforma_id).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching proforma items: {e}")
        return []

async def create_proforma_items(items_data):
    """Create proforma items"""
    try:
        response = supabase.table("proforma_items").insert(items_data).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error creating proforma items: {e}")
        raise

async def delete_proforma_items(proforma_id):
    """Delete all items for proforma"""
    try:
        response = supabase.table("proforma_items").delete().eq("proforma_id", proforma_id).execute()
        return True
    except Exception as e:
        print(f"Error deleting proforma items: {e}")
        raise

# ============================================================================
# INVOICES - Database operations
# ============================================================================

async def get_invoices():
    """Get all final invoices"""
    try:
        response = supabase.table("invoices").select("*").order("invoice_date", desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching invoices: {e}")
        return []

async def get_invoice_by_id(invoice_id):
    """Get invoice by ID"""
    try:
        response = supabase.table("invoices").select("*").eq("id", invoice_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error fetching invoice: {e}")
        return None

async def get_invoices_by_customer(customer_id):
    """Get all invoices for customer"""
    try:
        response = supabase.table("invoices").select("*").eq("customer_id", customer_id).order("invoice_date", desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching customer invoices: {e}")
        return []

async def create_invoice(invoice_data):
    """Create final invoice"""
    try:
        response = supabase.table("invoices").insert(invoice_data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error creating invoice: {e}")
        raise

async def update_invoice(invoice_id, invoice_data):
    """Update invoice"""
    try:
        response = supabase.table("invoices").update(invoice_data).eq("id", invoice_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error updating invoice: {e}")
        raise

async def delete_invoice(invoice_id):
    """Delete invoice"""
    try:
        response = supabase.table("invoices").delete().eq("id", invoice_id).execute()
        return True
    except Exception as e:
        print(f"Error deleting invoice: {e}")
        raise

# ============================================================================
# INVOICE ITEMS - Database operations
# ============================================================================

async def get_invoice_items(invoice_id):
    """Get items for invoice"""
    try:
        response = supabase.table("invoice_items").select("*").eq("invoice_id", invoice_id).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching invoice items: {e}")
        return []

async def create_invoice_items(items_data):
    """Create invoice items"""
    try:
        response = supabase.table("invoice_items").insert(items_data).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error creating invoice items: {e}")
        raise

async def delete_invoice_items(invoice_id):
    """Delete all items for invoice"""
    try:
        response = supabase.table("invoice_items").delete().eq("invoice_id", invoice_id).execute()
        return True
    except Exception as e:
        print(f"Error deleting invoice items: {e}")
        raise

async def get_patient_invoices(name_filter=None, invoice_type="patient"):
    """Get invoices filtered by type with optional name filtering"""
    try:
        query = supabase.table("invoices").select(
            "id, invoice_number, invoice_no, invoice_date, customer_id, customer_name, "
            "customer_phone, grand_total, payment_status, amount_received, payment_mode, items, notes, type"
        ).eq("type", invoice_type).order("invoice_date", desc=True)

        if name_filter:
            query = query.ilike("customer_name", f"%{name_filter}%")

        response = query.execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching invoices: {e}")
        return []

# ============================================================================
# STOCK LEDGER - Database operations
# ============================================================================

async def get_stock_ledger():
    """Get all stock ledger entries"""
    try:
        response = supabase.table("stock_ledger").select("*").order("created_at", desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching stock ledger: {e}")
        return []

async def get_product_stock(product_id):
    """Get current stock for product"""
    try:
        response = supabase.table("stock_ledger").select("change_qty").eq("product_id", product_id).execute()
        items = response.data if response.data else []
        total_stock = sum(item["change_qty"] for item in items)
        return total_stock
    except Exception as e:
        print(f"Error calculating product stock: {e}")
        return 0

async def add_stock_ledger_entry(product_id, change_qty, reason, reference_id=None, notes=None):
    """Add stock ledger entry"""
    try:
        entry_data = {
            "product_id": product_id,
            "change_qty": change_qty,
            "reason": reason,
            "reference_id": reference_id,
            "notes": notes
        }
        response = supabase.table("stock_ledger").insert(entry_data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error adding stock ledger entry: {e}")
        raise

# ============================================================================
# HELPERS - Utility functions
# ============================================================================

async def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        vendors_count = len(await get_vendors())
        products_count = len(await get_products())
        customers_count = len(await get_customers())
        invoices = await get_invoices()
        total_revenue = sum(inv.get("grand_total", 0) for inv in invoices)

        # Get total stock quantity by summing all purchase items
        try:
            purchase_response = supabase.table("purchase_items").select("qty").execute()
            total_stock = sum(item.get("qty", 0) for item in purchase_response.data) if purchase_response.data else 0
        except:
            total_stock = 0

        # Count expiring soon (next 90 days)
        expiring_soon = 0

        return {
            "total_vendors": vendors_count,
            "total_products": products_count,
            "total_customers": customers_count,
            "total_stock": total_stock,
            "total_revenue": total_revenue,
            "total_sales": len(invoices),
            "expiring_soon": expiring_soon
        }
    except Exception as e:
        print(f"Error getting dashboard stats: {e}")
        return {}

# ============================================================================
# SALES - Database operations
# ============================================================================

async def get_sales():
    """Get all sales records"""
    try:
        response = supabase.table("sales").select("*").order("sale_date", desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching sales: {e}")
        return []

async def create_sale(sale_data):
    """Create new sale record"""
    try:
        response = supabase.table("sales").insert(sale_data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error creating sale: {e}")
        raise

async def get_sale_by_id(sale_id):
    """Get sale by ID"""
    try:
        response = supabase.table("sales").select("*").eq("id", sale_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error fetching sale: {e}")
        return None

# ============================================================================
# EXPIRY - Helper functions
# ============================================================================

async def get_expiring_items(days_ahead=None):
    """Get all items with expiry dates (frontend filters by date range)"""
    try:
        from datetime import datetime, timedelta, date as date_type

        # Get all purchase items with expiry dates
        response = supabase.table("purchase_items").select("*").execute()
        items = response.data if response.data else []

        # Get all products for lookup
        products = await get_products()
        product_map = {p["id"]: p for p in products}

        # Get all invoice items from JSONB (items stored in invoices table)
        invoices_response = supabase.table("invoices").select("*").execute()
        invoices = invoices_response.data if invoices_response.data else []
        invoice_items = []
        for inv in invoices:
            for item in inv.get("items", []):
                invoice_items.append(item)

        # Get all draft items from JSONB (items stored in drafts table)
        drafts_response = supabase.table("drafts").select("*").execute()
        drafts = drafts_response.data if drafts_response.data else []
        draft_items = []
        for draft in drafts:
            for item in draft.get("items", []):
                draft_items.append(item)

        now = datetime.now()
        today = now.date() if isinstance(now, datetime) else now

        expiring = []
        for item in items:
            if item.get("expiry"):
                try:
                    # Handle both date string and date object
                    expiry = item["expiry"]
                    if isinstance(expiry, str):
                        expiry_date = datetime.strptime(expiry, "%Y-%m-%d").date()
                    else:
                        expiry_date = expiry if isinstance(expiry, date_type) else datetime.fromisoformat(str(expiry)).date()

                    # Calculate sold and reserved quantities for this batch
                    sold = sum(inv.get("qty", 0) for inv in invoice_items
                              if inv.get("product_id") == item.get("product_id")
                              and inv.get("batch") == item.get("batch"))

                    # Only count draft items as reserved (proformas no longer stored)
                    reserved = sum(d.get("qty", 0) for d in draft_items
                                  if d.get("product_id") == item.get("product_id")
                                  and d.get("batch") == item.get("batch"))

                    available = max(0, item.get("qty", 0) - sold - reserved)

                    # Include all items with expiry info and available stock
                    if available > 0:
                        product = product_map.get(item.get("product_id"), {})
                        days_diff = (expiry_date - today).days

                        expiring.append({
                            "id": item.get("id"),
                            "product_id": item.get("product_id"),
                            "product_name": product.get("name", "Unknown"),
                            "batch": item.get("batch"),
                            "expiry_date": expiry_date.isoformat() if isinstance(expiry_date, date_type) else str(expiry_date),
                            "quantity": available,
                            "total_quantity": item.get("qty", 0),
                            "sold": sold,
                            "reserved": reserved,
                            "mrp": float(product.get("mrp", 0)) if product.get("mrp") else 0,
                            "cost_price": float(product.get("cost_price", 0)) if product.get("cost_price") else 0,
                            "days_until_expiry": days_diff,
                            "is_expired": days_diff < 0
                        })
                except Exception as e:
                    print(f"Error processing item {item.get('id')}: {e}")
                    continue

        # Sort by days until expiry (ascending, expired items first)
        expiring.sort(key=lambda x: (x["days_until_expiry"], x["product_name"]))
        return expiring
    except Exception as e:
        print(f"Error getting expiring items: {e}")
        import traceback
        traceback.print_exc()
        return []

async def get_stock_summary_fast():
    """Get stock summary with TRUE batch queries (no N+1)"""
    try:
        products = await get_products()
        if not products:
            return []

        # Fetch ALL purchase items ONCE (not per product)
        try:
            purchase_response = supabase.table("purchase_items").select("product_id,qty,batch,expiry,created_at").order("created_at", desc=True).execute()
            all_purchase_items = purchase_response.data if purchase_response.data else []
        except Exception as e:
            print(f"Error fetching purchase items: {e}")
            all_purchase_items = []

        # Fetch invoices ONCE
        invoices = await get_invoices()

        # Group purchase items by product_id
        purchase_map = {}
        latest_map = {}
        for item in all_purchase_items:
            prod_id = item.get("product_id")
            if prod_id:
                if prod_id not in purchase_map:
                    purchase_map[prod_id] = []
                    latest_map[prod_id] = item  # First item is latest (already ordered desc)
                purchase_map[prod_id].append(item)

        # Build sold items map
        sold_map = {}
        for invoice in invoices:
            for item in invoice.get("items", []):
                prod_id = item.get("product_id")
                if prod_id:
                    if prod_id not in sold_map:
                        sold_map[prod_id] = 0
                    sold_map[prod_id] += item.get("qty", 0)

        # Build stock summary
        stock_summary = []
        for product in products:
            product_id = product["id"]

            # Get purchased qty from grouped data
            purchased_items = purchase_map.get(product_id, [])
            purchased = sum(item.get("qty", 0) for item in purchased_items)

            # Get sold qty from map
            sold = sold_map.get(product_id, 0)

            # Get latest batch/expiry from map
            latest_item = latest_map.get(product_id)
            latest_batch = latest_item.get("batch") if latest_item else None
            latest_expiry = latest_item.get("expiry") if latest_item else None

            available = purchased - sold

            stock_summary.append({
                "product_id": product_id,
                "product_name": product.get("name"),
                "purchased": purchased,
                "sold": sold,
                "available": max(0, available),
                "cost_price": product.get("cost_price"),
                "mrp": product.get("mrp"),
                "hsn_code": product.get("hsn_code"),
                "pack": product.get("pack"),
                "company": product.get("company"),
                "scheme": product.get("scheme"),
                "gst_rate": product.get("gst_rate"),
                "batch_no": latest_batch,
                "expiry_date": latest_expiry
            })

        return stock_summary
    except Exception as e:
        print(f"Error getting stock summary: {e}")
        import traceback
        traceback.print_exc()
        return []
