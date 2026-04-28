"""
Complete Supabase Integration for Graftcare - Production Ready
All endpoints connected to Supabase database
UI → FastAPI → Supabase flow
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from pathlib import Path
from datetime import datetime, date, timedelta
from uuid import uuid4
from dotenv import load_dotenv
import time
import os
import shutil

from backend.supabase_client import (
    supabase,
    get_vendors, create_vendor, update_vendor, delete_vendor, get_vendor_by_gstin, get_vendor_by_phone, get_vendor_by_id,
    get_products, create_product, update_product, delete_product, get_product_by_id,
    get_customers, create_customer, update_customer, delete_customer, get_customer_by_id, get_customer_by_phone, get_customer_by_gstin,
    get_purchase_invoices, create_purchase_invoice, update_purchase_invoice, delete_purchase_invoice, get_purchase_invoice_by_id, get_purchase_invoices_by_vendor,
    get_purchase_items, create_purchase_items, delete_purchase_items,
    get_drafts, create_draft, update_draft, delete_draft, get_draft_by_id, lookup_draft_by_phone, lookup_draft_by_gstin, count_drafts_by_phone,
    get_invoices, create_invoice, update_invoice, delete_invoice, get_invoice_by_id, get_invoices_by_customer, get_patient_invoices,
    get_stock_ledger, add_stock_ledger_entry, get_product_stock, get_dashboard_stats, get_stock_summary_fast,
    get_sales, create_sale, get_expiring_items
)

load_dotenv()

app = FastAPI(title="Graftcare API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cache for stock summary (refresh every 30 seconds)
_stock_cache = {"data": None, "timestamp": 0}
STOCK_CACHE_TTL = 30  # seconds

# Cache for products list (refresh every 60 seconds)
_products_cache = {"data": None, "timestamp": 0}
PRODUCTS_CACHE_TTL = 60  # seconds

# Cache for purchase invoices (refresh every 30 seconds)
_purchase_invoices_cache = {"data": None, "timestamp": 0}
PURCHASE_INVOICES_CACHE_TTL = 30  # seconds

# Cache for patient tracker (refresh every 30 seconds)
_patient_tracker_cache = {"data": None, "timestamp": 0}
PATIENT_TRACKER_CACHE_TTL = 30  # seconds

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class VendorModel(BaseModel):
    id: Optional[str] = None
    name: str
    contact_person: Optional[str] = None
    phone: str
    gstin: str
    dl1: Optional[str] = None
    dl2: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None
    bank_name: Optional[str] = None
    bank_acc: Optional[str] = None
    bank_ifsc: Optional[str] = None

class ProductModel(BaseModel):
    id: Optional[str] = None
    name: str
    hsn_code: Optional[str] = None
    pack: Optional[str] = None
    company: Optional[str] = None
    scheme: Optional[str] = None
    cost_price: float
    mrp: float
    gst_rate: float

class ProductUpdateModel(BaseModel):
    name: Optional[str] = None
    hsn_code: Optional[str] = None
    pack: Optional[str] = None
    company: Optional[str] = None
    scheme: Optional[str] = None
    cost_price: Optional[float] = None
    mrp: Optional[float] = None
    gst_rate: Optional[float] = None

class CustomerModel(BaseModel):
    id: Optional[str] = None
    name: str
    contact_person: Optional[str] = None
    phone: str
    gstin: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None
    customer_type: str = "retailer"
    credit_limit: float = 0.0
    outstanding_balance: float = 0.0
    # Additional fields for Retailer
    door_number: Optional[str] = None
    dl1: Optional[str] = None
    dl2: Optional[str] = None
    state: Optional[str] = None
    # Additional fields for Patient
    age: Optional[str] = None
    gender: Optional[str] = None
    doctor_name: Optional[str] = None
    hospital_name: Optional[str] = None
    doctor_phone: Optional[str] = None
    is_member: Optional[bool] = False
    member_id: Optional[str] = None

class PurchaseInvoiceModel(BaseModel):
    id: Optional[str] = None
    vendor_id: str
    vendor_invoice_no: str
    invoice_date: str
    payment_mode: Optional[str] = None
    amount_paid: Optional[float] = None
    paid_by: Optional[str] = None
    transaction_id: Optional[str] = None
    subtotal: Optional[float] = None
    total_gst: Optional[float] = None
    discount_amount: Optional[float] = None
    grand_total: float
    payment_status: str = "pending"
    notes: Optional[str] = None
    items: List[Dict[str, Any]] = []

class PurchaseItemModel(BaseModel):
    product_id: str
    qty: int
    batch: str
    expiry: str
    mrp: Optional[float] = None
    buy_rate: Optional[float] = None
    free: int = 0
    discount: Optional[float] = None
    gst: Optional[float] = None

class DraftModel(BaseModel):
    id: Optional[str] = None
    type: str = "patient"           # 'retailer' or 'patient'
    draft_counter: Optional[int] = None
    # Common customer fields
    customer_name: str
    customer_phone: str
    customer_address: Optional[str] = None
    customer_city: Optional[str] = None
    customer_pincode: Optional[str] = None
    customer_state: Optional[str] = None
    customer_door_number: Optional[str] = None
    # Retailer-specific
    customer_gstin: Optional[str] = None
    customer_dl1: Optional[str] = None
    customer_dl2: Optional[str] = None
    # Patient-specific
    customer_age: Optional[str] = None
    customer_gender: Optional[str] = None
    customer_doctor_name: Optional[str] = None
    customer_hospital_name: Optional[str] = None
    customer_doctor_phone: Optional[str] = None
    customer_is_member: Optional[bool] = False
    customer_member_id: Optional[str] = None
    # Invoice totals
    subtotal: Optional[float] = None
    total_gst: Optional[float] = None
    discount_amount: Optional[float] = None
    discount_type: Optional[str] = "pct"  # 'pct' or 'amt'
    discount_value: Optional[float] = 0
    charity_amount: Optional[float] = None
    grand_total: Optional[float] = None
    notes: Optional[str] = None
    items: List[Dict[str, Any]] = []  # All items stored as JSONB array

class InvoiceModel(BaseModel):
    id: Optional[str] = None
    customer_id: str  # References customers table (final invoice only)
    invoice_date: Optional[str] = None
    invoice_no: Optional[str] = None
    subtotal: Optional[float] = None
    total_gst: Optional[float] = None
    discount_amount: Optional[float] = None
    grand_total: Optional[float] = None
    payment_mode: Optional[str] = None
    amount_received: Optional[float] = None
    payment_status: str = "pending"
    notes: Optional[str] = None
    items: List[Dict[str, Any]] = []  # All items stored as JSONB array

class SalesModel(BaseModel):
    id: Optional[str] = None
    customer_name: str
    customer_phone: Optional[str] = None
    product_id: str
    quantity: int
    selling_price: float
    sale_date: str
    notes: Optional[str] = None

# ============================================================================
# STATES - Indian States & Union Territories
# ============================================================================

INDIAN_STATES = [
    {"code": "AP", "name": "Andhra Pradesh"},
    {"code": "AR", "name": "Arunachal Pradesh"},
    {"code": "AS", "name": "Assam"},
    {"code": "BR", "name": "Bihar"},
    {"code": "CG", "name": "Chhattisgarh"},
    {"code": "GA", "name": "Goa"},
    {"code": "GJ", "name": "Gujarat"},
    {"code": "HR", "name": "Haryana"},
    {"code": "HP", "name": "Himachal Pradesh"},
    {"code": "JK", "name": "Jammu and Kashmir"},
    {"code": "JH", "name": "Jharkhand"},
    {"code": "KA", "name": "Karnataka"},
    {"code": "KL", "name": "Kerala"},
    {"code": "MP", "name": "Madhya Pradesh"},
    {"code": "MH", "name": "Maharashtra"},
    {"code": "MN", "name": "Manipur"},
    {"code": "ML", "name": "Meghalaya"},
    {"code": "MZ", "name": "Mizoram"},
    {"code": "NL", "name": "Nagaland"},
    {"code": "OR", "name": "Odisha"},
    {"code": "PB", "name": "Punjab"},
    {"code": "RJ", "name": "Rajasthan"},
    {"code": "SK", "name": "Sikkim"},
    {"code": "TN", "name": "Tamil Nadu"},
    {"code": "TG", "name": "Telangana"},
    {"code": "TR", "name": "Tripura"},
    {"code": "UP", "name": "Uttar Pradesh"},
    {"code": "UT", "name": "Uttarakhand"},
    {"code": "WB", "name": "West Bengal"},
]

@app.get("/api/states")
async def get_states():
    """Get all Indian states and union territories"""
    return INDIAN_STATES

# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# ============================================================================
# VENDORS ENDPOINTS
# ============================================================================

@app.get("/api/vendors")
async def get_all_vendors():
    """Get all vendors"""
    try:
        vendors = await get_vendors()
        return vendors
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/vendors/{vendor_id}")
async def get_vendor(vendor_id: str):
    """Get vendor by ID"""
    try:
        vendor = await get_vendor_by_id(vendor_id)
        if not vendor:
            raise HTTPException(status_code=404, detail="Vendor not found")
        return vendor
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/vendors")
async def create_new_vendor(vendor: VendorModel):
    """Create new vendor"""
    try:
        if vendor.phone:
            existing = await get_vendor_by_phone(vendor.phone)
            if existing:
                raise HTTPException(status_code=400, detail="Phone number already exists")

        if vendor.gstin:
            existing = await get_vendor_by_gstin(vendor.gstin)
            if existing:
                raise HTTPException(status_code=400, detail="GSTIN already exists")

        result = await create_vendor(vendor.dict(exclude_none=True))
        return {"id": result["id"], "message": "Vendor created successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/vendors/{vendor_id}")
async def update_existing_vendor(vendor_id: str, vendor: VendorModel):
    """Update vendor"""
    try:
        existing_vendor = await get_vendor_by_id(vendor_id)
        if not existing_vendor:
            raise HTTPException(status_code=404, detail="Vendor not found")

        if vendor.phone and vendor.phone != existing_vendor.get("phone"):
            dup = await get_vendor_by_phone(vendor.phone)
            if dup:
                raise HTTPException(status_code=400, detail="Phone number already in use")

        if vendor.gstin and vendor.gstin != existing_vendor.get("gstin"):
            dup = await get_vendor_by_gstin(vendor.gstin)
            if dup:
                raise HTTPException(status_code=400, detail="GSTIN already in use")

        await update_vendor(vendor_id, vendor.dict(exclude_none=True))
        return {"message": "Vendor updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/vendors/phone/{phone}")
async def get_vendor_by_phone_route(phone: str):
    """Get vendor by phone number"""
    try:
        vendor = await get_vendor_by_phone(phone)
        if not vendor:
            return {}
        return vendor
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/vendors/gstin/{gstin}")
async def get_vendor_by_gstin_route(gstin: str):
    """Get vendor by GSTIN - used for Purchase Invoice to check if vendor exists"""
    try:
        vendor = await get_vendor_by_gstin(gstin)
        if not vendor:
            return {}
        return vendor
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/vendors/{vendor_id}/invoices")
async def get_vendor_invoices(vendor_id: str):
    """Get all purchase invoices for a vendor"""
    try:
        invoices = await get_purchase_invoices_by_vendor(vendor_id)
        return invoices if invoices else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/vendors/{vendor_id}/details")
async def get_vendor_details(vendor_id: str):
    """Get vendor details with purchase summary"""
    try:
        vendor = await get_vendor_by_id(vendor_id)
        if not vendor:
            raise HTTPException(status_code=404, detail="Vendor not found")

        invoices = await get_purchase_invoices_by_vendor(vendor_id)

        total_amount = sum(inv.get('grand_total', 0) for inv in invoices) if invoices else 0

        return {
            **vendor,
            "total_purchases": len(invoices),
            "total_amount": total_amount,
            "purchases": invoices
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/vendors/{vendor_id}")
async def delete_existing_vendor(vendor_id: str):
    """Delete vendor"""
    try:
        vendor = await get_vendor_by_id(vendor_id)
        if not vendor:
            raise HTTPException(status_code=404, detail="Vendor not found")
        await delete_vendor(vendor_id)
        return {"message": "Vendor deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# PRODUCTS ENDPOINTS
# ============================================================================

@app.get("/api/products")
async def get_all_products():
    """Get all products - with caching"""
    try:
        current_time = time.time()
        # Return cached data if still fresh
        if _products_cache["data"] is not None and (current_time - _products_cache["timestamp"]) < PRODUCTS_CACHE_TTL:
            return _products_cache["data"]

        # Fetch fresh data
        products = await get_products()
        _products_cache["data"] = products
        _products_cache["timestamp"] = current_time
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/products/{product_id}")
async def get_product(product_id: str):
    """Get product by ID"""
    try:
        product = await get_product_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/products")
async def create_new_product(product: ProductModel):
    """Create new product"""
    try:
        result = await create_product(product.dict(exclude_none=True))
        # Invalidate products cache since new product added
        _products_cache["data"] = None
        _products_cache["timestamp"] = 0
        return {"id": result["id"], "message": "Product created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/products/{product_id}")
async def update_existing_product(product_id: str, product: ProductUpdateModel):
    """Update product (partial fields allowed)"""
    try:
        existing = await get_product_by_id(product_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Product not found")
        await update_product(product_id, product.dict(exclude_none=True))
        # Invalidate products cache since product updated
        _products_cache["data"] = None
        _products_cache["timestamp"] = 0
        return {"message": "Product updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/products/{product_id}")
async def delete_existing_product(product_id: str):
    """Delete product"""
    try:
        product = await get_product_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        await delete_product(product_id)
        return {"message": "Product deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# CUSTOMERS ENDPOINTS
# ============================================================================

@app.get("/api/customers")
async def get_all_customers():
    """Get all customers"""
    try:
        customers = await get_customers()
        return customers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/customers/{customer_id}")
async def get_customer(customer_id: str):
    """Get customer by ID"""
    try:
        customer = await get_customer_by_id(customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/customers/phone/{phone}")
async def get_customer_by_phone_route(phone: str):
    """Get customer by phone number - used for Draft/Proforma to check if customer exists (works for both retailer and patient)"""
    try:
        customer = await get_customer_by_phone(phone)
        if not customer:
            return {}
        return customer
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/customers")
async def create_new_customer(customer: CustomerModel):
    """Create new customer"""
    try:
        if customer.phone:
            existing = await get_customer_by_phone(customer.phone)
            if existing:
                raise HTTPException(status_code=400, detail="Phone number already exists")

        if customer.gstin:
            existing = await get_customer_by_gstin(customer.gstin)
            if existing:
                raise HTTPException(status_code=400, detail="GSTIN already exists")

        result = await create_customer(customer.dict(exclude_none=True))
        return {"id": result["id"], "message": "Customer created successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/customers/{customer_id}")
async def update_existing_customer(customer_id: str, customer: CustomerModel):
    """Update customer"""
    try:
        existing_customer = await get_customer_by_id(customer_id)
        if not existing_customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        if customer.phone and customer.phone != existing_customer.get("phone"):
            dup = await get_customer_by_phone(customer.phone)
            if dup:
                raise HTTPException(status_code=400, detail="Phone number already in use")

        if customer.gstin and customer.gstin != existing_customer.get("gstin"):
            dup = await get_customer_by_gstin(customer.gstin)
            if dup:
                raise HTTPException(status_code=400, detail="GSTIN already in use")

        await update_customer(customer_id, customer.dict(exclude_none=True))
        return {"message": "Customer updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/customers/{customer_id}")
async def delete_existing_customer(customer_id: str):
    """Delete customer"""
    try:
        customer = await get_customer_by_id(customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        await delete_customer(customer_id)
        return {"message": "Customer deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# PURCHASE INVOICES ENDPOINTS
# ============================================================================

@app.get("/api/purchase-invoices")
async def get_all_purchase_invoices():
    """Get all purchase invoices - with caching and batch queries"""
    try:
        current_time = time.time()
        # Return cached data if still fresh
        if _purchase_invoices_cache["data"] is not None and (current_time - _purchase_invoices_cache["timestamp"]) < PURCHASE_INVOICES_CACHE_TTL:
            return _purchase_invoices_cache["data"]

        # Fetch invoices
        invoices = await get_purchase_invoices()

        # Fetch ALL purchase items at once (not per invoice)
        try:
            all_items_response = supabase.table("purchase_items").select("*").execute()
            all_items = all_items_response.data if all_items_response.data else []
        except Exception as e:
            print(f"Error fetching purchase items: {e}")
            all_items = []

        # Group items by invoice_id for fast lookup
        items_by_invoice = {}
        for item in all_items:
            inv_id = item.get("purchase_invoice_id")
            if inv_id:
                if inv_id not in items_by_invoice:
                    items_by_invoice[inv_id] = []
                items_by_invoice[inv_id].append(item)

        # Add items to invoices
        for inv in invoices:
            inv["items"] = items_by_invoice.get(inv["id"], [])

        # Cache the result
        _purchase_invoices_cache["data"] = invoices
        _purchase_invoices_cache["timestamp"] = current_time
        return invoices
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/purchase-invoices/{invoice_id}")
async def get_purchase_invoice(invoice_id: str):
    """Get purchase invoice by ID"""
    try:
        invoice = await get_purchase_invoice_by_id(invoice_id)
        if not invoice:
            raise HTTPException(status_code=404, detail="Purchase invoice not found")
        invoice["items"] = await get_purchase_items(invoice_id)
        return invoice
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/purchase-invoices")
async def create_new_purchase_invoice(invoice: PurchaseInvoiceModel):
    """Create purchase invoice with items and stock update - optimized"""
    try:
        vendor = await get_vendor_by_id(invoice.vendor_id)
        if not vendor:
            raise HTTPException(status_code=404, detail="Vendor not found")

        # Prepare invoice data with items as JSONB array
        invoice_data = invoice.dict(exclude_none=True)
        # Ensure items are included in the invoice
        if invoice.items:
            invoice_data["items"] = invoice.items

        created_invoice = await create_purchase_invoice(invoice_data)

        # Invalidate purchase invoices cache
        _purchase_invoices_cache["data"] = None
        _purchase_invoices_cache["timestamp"] = 0

        if invoice.items:
            # Batch fetch all products at once (not per item)
            products = await get_products()
            product_map = {p["id"]: p for p in products}

            # Validate all products exist
            for item in invoice.items:
                if item["product_id"] not in product_map:
                    raise HTTPException(status_code=404, detail=f"Product not found: {item['product_id']}")

            # Prepare all items to insert
            items_to_insert = []
            ledger_entries = []

            for item in invoice.items:
                item_data = {
                    "purchase_invoice_id": created_invoice["id"],
                    "product_id": item["product_id"],
                    "qty": item["qty"],
                    "batch": item["batch"],
                    "expiry": item["expiry"],
                    "mrp": item.get("mrp"),
                    "buy_rate": item.get("buy_rate"),
                    "free": item.get("free", 0),
                    "discount": item.get("discount"),
                    "gst": item.get("gst")
                }
                items_to_insert.append(item_data)

                # Prepare ledger entry (batch insert later)
                ledger_entries.append({
                    "product_id": item["product_id"],
                    "change_qty": item["qty"],
                    "reason": "purchase",
                    "reference_id": created_invoice["id"]
                })

            # Batch insert items
            if items_to_insert:
                await create_purchase_items(items_to_insert)

            # Batch insert stock ledger entries
            if ledger_entries:
                try:
                    supabase.table("stock_ledger").insert(ledger_entries).execute()
                except Exception as e:
                    print(f"Error inserting stock ledger entries: {e}")
                    # Continue even if ledger insert fails

        return {"id": created_invoice["id"], "message": "Purchase invoice created successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/purchase-invoices/{invoice_id}")
async def update_existing_purchase_invoice(invoice_id: str, invoice: PurchaseInvoiceModel):
    """Update purchase invoice"""
    try:
        existing = await get_purchase_invoice_by_id(invoice_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Purchase invoice not found")

        invoice_data = invoice.dict(exclude={"items"}, exclude_none=True)
        await update_purchase_invoice(invoice_id, invoice_data)

        return {"message": "Purchase invoice updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/purchase-invoices/{invoice_id}")
async def delete_existing_purchase_invoice(invoice_id: str):
    """Delete purchase invoice and remove stock"""
    try:
        invoice = await get_purchase_invoice_by_id(invoice_id)
        if not invoice:
            raise HTTPException(status_code=404, detail="Purchase invoice not found")

        items = await get_purchase_items(invoice_id)
        for item in items:
            await add_stock_ledger_entry(
                product_id=item["product_id"],
                change_qty=-item["qty"],
                reason="purchase_reversal",
                reference_id=invoice_id
            )

        await delete_purchase_items(invoice_id)
        await delete_purchase_invoice(invoice_id)
        return {"message": "Purchase invoice deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# PURCHASE INVOICE PDF ENDPOINTS
# ============================================================================

@app.post("/api/purchase-invoices/{invoice_id}/upload-pdf")
async def upload_purchase_invoice_pdf(invoice_id: str, file: UploadFile = File(...)):
    """Upload PDF file for purchase invoice to Supabase Storage"""
    try:
        # Verify invoice exists
        invoice = await get_purchase_invoice_by_id(invoice_id)
        if not invoice:
            raise HTTPException(status_code=404, detail="Purchase invoice not found")

        # Read file contents
        contents = await file.read()

        # Upload to Supabase Storage (purchase-invoices bucket)
        file_path = f"pdfs/{invoice_id}.pdf"
        try:
            supabase.storage.from_("purchase-invoices").upload(file_path, contents)
        except Exception as upload_err:
            # If bucket doesn't exist, try creating it first
            if "not found" in str(upload_err).lower():
                supabase.storage.create_bucket("purchase-invoices", options={"public": True})
                supabase.storage.from_("purchase-invoices").upload(file_path, contents)
            else:
                raise

        # Update invoice with pdf_file_path
        pdf_path = f"pdfs/{invoice_id}.pdf"
        await update_purchase_invoice(invoice_id, {"pdf_file_path": pdf_path})

        return {"message": "PDF uploaded successfully", "file_path": pdf_path}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/purchase-invoices/{invoice_id}/pdf")
async def download_purchase_invoice_pdf(invoice_id: str):
    """Download PDF file for purchase invoice from Supabase Storage"""
    try:
        # Verify invoice exists
        invoice = await get_purchase_invoice_by_id(invoice_id)
        if not invoice:
            raise HTTPException(status_code=404, detail="Purchase invoice not found")

        # Try to download from Supabase Storage
        file_path = f"pdfs/{invoice_id}.pdf"
        try:
            pdf_data = supabase.storage.from_("purchase-invoices").download(file_path)
            return StreamingResponse(
                iter([pdf_data]),
                media_type="application/pdf",
                headers={"Content-Disposition": f"attachment; filename=purchase_invoice_{invoice_id}.pdf"}
            )
        except Exception as storage_err:
            # If not found in Supabase, check local storage for backward compatibility
            local_path = Path("storage/pdfs") / f"{invoice_id}.pdf"
            if local_path.exists():
                return FileResponse(
                    path=local_path,
                    media_type="application/pdf",
                    filename=f"purchase_invoice_{invoice_id}.pdf"
                )

            # Check for old naming pattern (invoice_id_hash.pdf)
            import glob
            old_pattern_files = list(Path("storage/pdfs").glob(f"{invoice_id}_*.pdf"))
            if old_pattern_files:
                return FileResponse(
                    path=old_pattern_files[0],
                    media_type="application/pdf",
                    filename=f"purchase_invoice_{invoice_id}.pdf"
                )

            raise HTTPException(status_code=404, detail="PDF file not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# DRAFTS ENDPOINTS
# ============================================================================

@app.get("/api/drafts")
async def get_all_drafts():
    """Get all draft invoices (items already in JSONB)"""
    try:
        drafts = await get_drafts()
        return drafts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/drafts/lookup")
async def lookup_draft(phone: str, type: str = "patient", gstin: Optional[str] = None):
    """Look up existing draft by phone and type (or by GSTIN for retailers)"""
    try:
        # First, try lookup by phone + type
        draft = await lookup_draft_by_phone(phone, type)

        # If not found and retailer with GSTIN, try lookup by GSTIN
        if not draft and type == "retailer" and gstin:
            draft = await lookup_draft_by_gstin(gstin)

        if draft:
            return draft
        else:
            return {"found": False}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/drafts/{draft_id}")
async def get_draft(draft_id: str):
    """Get draft by ID (items already in JSONB)"""
    try:
        draft = await get_draft_by_id(draft_id)
        if not draft:
            raise HTTPException(status_code=404, detail="Draft not found")
        return draft
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/drafts")
async def create_new_draft(draft: DraftModel):
    """Create draft invoice with all data stored in individual columns"""
    try:
        # Validate items and enrich with product details
        enriched_items = []
        for item in draft.items:
            product = await get_product_by_id(item.get("product_id"))
            if not product:
                raise HTTPException(status_code=404, detail=f"Product not found: {item.get('product_id')}")

            enriched_item = {
                **item,
                "product_name": item.get("product_name") or product.get("name"),
                "company": item.get("company") or product.get("company"),
                "hsn_code": item.get("hsn_code") or product.get("hsn_code"),
                "pack": item.get("pack") or product.get("pack"),
                "scheme": item.get("scheme") or product.get("scheme"),
                "cost_price": item.get("cost_price") or product.get("cost_price"),
                "mrp": item.get("mrp") or product.get("mrp")
            }
            enriched_items.append(enriched_item)

        # Calculate draft counter: count existing drafts for this phone + 1
        existing_count = await count_drafts_by_phone(draft.customer_phone)
        draft_counter = existing_count + 1

        # Prepare draft data with all fields flattened
        draft_data = draft.dict(exclude={"id", "draft_counter"}, exclude_none=True)
        draft_data["draft_counter"] = draft_counter
        draft_data["items"] = enriched_items

        created_draft = await create_draft(draft_data)
        return {"id": created_draft["id"], "message": "Draft created successfully", "draft_counter": draft_counter}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/drafts/{draft_id}")
async def update_existing_draft(draft_id: str, draft: DraftModel):
    """Update draft invoice with all data stored as JSONB"""
    try:
        existing = await get_draft_by_id(draft_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Draft not found")

        # Validate items and enrich with product details
        enriched_items = []
        for item in draft.items:
            product = await get_product_by_id(item.get("product_id"))
            if not product:
                raise HTTPException(status_code=404, detail=f"Product not found: {item.get('product_id')}")

            enriched_item = {
                **item,
                "product_name": item.get("product_name") or product.get("name"),
                "company": item.get("company") or product.get("company"),
                "hsn_code": item.get("hsn_code") or product.get("hsn_code"),
                "pack": item.get("pack") or product.get("pack"),
                "scheme": item.get("scheme") or product.get("scheme"),
                "cost_price": item.get("cost_price") or product.get("cost_price"),
                "mrp": item.get("mrp") or product.get("mrp")
            }
            enriched_items.append(enriched_item)

        # Update draft with enriched items and customer data
        draft_data = draft.dict(exclude={"id"}, exclude_none=True)
        draft_data["items"] = enriched_items

        await update_draft(draft_id, draft_data)
        return {"message": "Draft updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/drafts/{draft_id}")
async def delete_existing_draft(draft_id: str):
    """Delete draft invoice"""
    try:
        draft = await get_draft_by_id(draft_id)
        if not draft:
            raise HTTPException(status_code=404, detail="Draft not found")
        await delete_draft(draft_id)
        return {"message": "Draft deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/drafts/{draft_id}/to-invoice")
async def draft_to_invoice(draft_id: str):
    """Convert draft to final invoice: create/update customer + create invoice + delete draft"""
    try:
        draft = await get_draft_by_id(draft_id)
        if not draft:
            raise HTTPException(status_code=404, detail="Draft not found")

        # Validate required customer fields
        if not draft.get("customer_phone"):
            raise HTTPException(status_code=400, detail="Draft has no customer phone")

        # Build customer object from flat columns
        customer_data_for_invoice = {
            "name": draft.get("customer_name"),
            "phone": draft.get("customer_phone"),
            "customer_type": draft.get("type", "patient"),
            "address": draft.get("customer_address"),
            "city": draft.get("customer_city"),
            "pincode": draft.get("customer_pincode"),
            "state": draft.get("customer_state"),
            "door_number": draft.get("customer_door_number"),
            "gstin": draft.get("customer_gstin"),
            "dl1": draft.get("customer_dl1"),
            "dl2": draft.get("customer_dl2"),
            "age": draft.get("customer_age"),
            "gender": draft.get("customer_gender"),
            "doctor_name": draft.get("customer_doctor_name"),
            "hospital_name": draft.get("customer_hospital_name"),
            "doctor_phone": draft.get("customer_doctor_phone"),
            "is_member": draft.get("customer_is_member", False),
            "member_id": draft.get("customer_member_id"),
        }

        # Create or update customer from draft data
        existing_customer = await get_customer_by_phone(customer_data_for_invoice["phone"])
        if existing_customer:
            customer_id = existing_customer["id"]
            # Update with latest customer data
            await update_customer(customer_id, customer_data_for_invoice)
        else:
            # Create new customer
            customer = await create_customer(customer_data_for_invoice)
            customer_id = customer["id"]

        # Create invoice with items from draft and all customer details
        # Generate invoice number: INV-YYYYMMDD-XXXX
        invoice_no = "INV-" + str(date.today()).replace("-", "") + "-" + str(uuid4())[:4].upper()

        invoice_data = {
            "customer_id": customer_id,
            "invoice_no": invoice_no,
            "invoice_date": str(date.today()),
            "subtotal": draft.get("subtotal"),
            "total_gst": draft.get("total_gst"),
            "discount_amount": draft.get("discount_amount"),
            "grand_total": draft.get("grand_total"),
            "notes": draft.get("notes"),
            "items": draft.get("items", []),
            # Copy all customer details to invoice (denormalized)
            "type": draft.get("type", "patient"),
            "customer_name": draft.get("customer_name"),
            "customer_phone": draft.get("customer_phone"),
            "customer_address": draft.get("customer_address"),
            "customer_city": draft.get("customer_city"),
            "customer_pincode": draft.get("customer_pincode"),
            "customer_state": draft.get("customer_state"),
            "customer_door_number": draft.get("customer_door_number"),
            "customer_gstin": draft.get("customer_gstin"),
            "customer_dl1": draft.get("customer_dl1"),
            "customer_dl2": draft.get("customer_dl2"),
            "customer_age": draft.get("customer_age"),
            "customer_gender": draft.get("customer_gender"),
            "customer_doctor_name": draft.get("customer_doctor_name"),
            "customer_hospital_name": draft.get("customer_hospital_name"),
            "customer_doctor_phone": draft.get("customer_doctor_phone"),
            "customer_is_member": draft.get("customer_is_member", False),
            "customer_member_id": draft.get("customer_member_id"),
        }
        created_invoice = await create_invoice(invoice_data)

        # Delete draft after successful invoice creation
        await delete_draft(draft_id)

        return {"id": created_invoice["id"], "message": "Draft converted to invoice successfully", "customer_id": customer_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# INVOICES ENDPOINTS
# ============================================================================

@app.get("/api/invoices")
async def get_all_invoices():
    """Get all final invoices (items already in JSONB)"""
    try:
        invoices = await get_invoices()
        return invoices
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/invoices/{invoice_id}")
async def get_invoice(invoice_id: str):
    """Get invoice by ID (items already in JSONB)"""
    try:
        invoice = await get_invoice_by_id(invoice_id)
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        return invoice
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/customers/{customer_id}/invoices")
async def get_customer_invoices(customer_id: str):
    """Get all invoices for customer (items already in JSONB)"""
    try:
        customer = await get_customer_by_id(customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        invoices = await get_invoices_by_customer(customer_id)
        return invoices
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/invoices/{invoice_id}")
async def update_existing_invoice(invoice_id: str, invoice: InvoiceModel):
    """Update invoice payment status"""
    try:
        existing = await get_invoice_by_id(invoice_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Invoice not found")

        update_data = {
            "payment_mode": invoice.payment_mode,
            "amount_received": invoice.amount_received,
            "payment_status": invoice.payment_status,
            "notes": invoice.notes
        }
        await update_invoice(invoice_id, update_data)
        return {"message": "Invoice updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/invoices/{invoice_id}")
async def delete_existing_invoice(invoice_id: str):
    """Delete invoice and restore stock"""
    try:
        invoice = await get_invoice_by_id(invoice_id)
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")

        # Get items from JSONB column
        items = invoice.get("items", [])
        for item in items:
            await add_stock_ledger_entry(
                product_id=item["product_id"],
                change_qty=item["qty"],
                reason="sale_reversal",
                reference_id=invoice_id
            )

        await delete_invoice(invoice_id)
        return {"message": "Invoice deleted and stock restored"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# PATIENT TRACKER ENDPOINTS
# ============================================================================

@app.get("/api/patient-tracker")
async def get_patient_tracker(name: str = None, type: str = "patient"):
    """Get invoices by type with optional name filtering - fast and cached"""
    try:
        current_time = time.time()

        # Only cache when no name filter (full list is stable)
        if not name and _patient_tracker_cache["data"] is not None and (current_time - _patient_tracker_cache["timestamp"]) < PATIENT_TRACKER_CACHE_TTL:
            return _patient_tracker_cache["data"]

        # Fetch invoices (filtered by type and optional name)
        invoices = await get_patient_invoices(name_filter=name, invoice_type=type)

        # Group invoices by customer_id for organized response
        patients_dict = {}
        for invoice in invoices:
            customer_id = invoice.get("customer_id")
            patient_name = invoice.get("customer_name", "Unknown")

            if customer_id not in patients_dict:
                patients_dict[customer_id] = {
                    "customer_id": customer_id,
                    "patient_name": patient_name,
                    "customer_phone": invoice.get("customer_phone"),
                    "total_invoices": 0,
                    "total_amount": 0,
                    "invoices": []
                }

            # Add invoice to patient's list
            patients_dict[customer_id]["invoices"].append({
                "id": invoice.get("id"),
                "invoice_number": invoice.get("invoice_number") or invoice.get("invoice_no"),
                "invoice_date": invoice.get("invoice_date"),
                "grand_total": invoice.get("grand_total"),
                "payment_status": invoice.get("payment_status"),
                "amount_received": invoice.get("amount_received"),
                "items": invoice.get("items", []),
                "notes": invoice.get("notes")
            })

            # Update totals
            patients_dict[customer_id]["total_invoices"] += 1
            patients_dict[customer_id]["total_amount"] += invoice.get("grand_total", 0)

        result = list(patients_dict.values())

        # Cache only when no name filter
        if not name:
            _patient_tracker_cache["data"] = result
            _patient_tracker_cache["timestamp"] = current_time

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/patient-tracker/invoice/{invoice_id}")
async def get_patient_invoice_details(invoice_id: str):
    """Get full details of a patient invoice"""
    try:
        invoice = await get_invoice_by_id(invoice_id)
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")

        # Verify it's a patient invoice
        if invoice.get("type") != "patient":
            raise HTTPException(status_code=403, detail="This is not a patient invoice")

        return {
            "id": invoice.get("id"),
            "customer_id": invoice.get("customer_id"),
            "invoice_number": invoice.get("invoice_number") or invoice.get("invoice_no"),
            "invoice_date": invoice.get("invoice_date"),
            "customer_name": invoice.get("customer_name"),
            "customer_phone": invoice.get("customer_phone"),
            "customer_address": invoice.get("customer_address"),
            "items": invoice.get("items", []),
            "subtotal": invoice.get("subtotal"),
            "total_gst": invoice.get("total_gst"),
            "discount_amount": invoice.get("discount_amount"),
            "grand_total": invoice.get("grand_total"),
            "payment_status": invoice.get("payment_status"),
            "amount_received": invoice.get("amount_received"),
            "payment_mode": invoice.get("payment_mode"),
            "notes": invoice.get("notes"),
            "created_at": invoice.get("created_at"),
            "type": invoice.get("type")
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/customer-names")
async def get_customer_names_suggestions(customer_type: str = "patient", q: str = ""):
    """Get unique customer names for autocomplete (filtered by type and name query)"""
    try:
        name_query = q.strip()

        # Get invoices filtered by type
        response = supabase.table("invoices").select("customer_name").eq("type", customer_type).execute()
        invoices = response.data if response.data else []

        # Extract unique customer names
        unique_names = list(set(inv.get("customer_name", "").strip() for inv in invoices if inv.get("customer_name")))
        unique_names.sort()

        # Filter by query if provided (case-insensitive partial match)
        if name_query:
            unique_names = [name for name in unique_names if name_query.lower() in name.lower()]

        # Limit to 10 suggestions
        return unique_names[:10]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/customer-details")
async def get_customer_details(customer_type: str = "patient", customer_name: str = ""):
    """Get complete customer details from invoices and drafts for that customer"""
    try:
        if not customer_name:
            raise HTTPException(status_code=400, detail="customer_name required")

        # Get all invoices for this customer
        inv_response = supabase.table("invoices").select("*").eq("type", customer_type).eq("customer_name", customer_name).order("invoice_date", desc=True).execute()
        invoices = inv_response.data if inv_response.data else []

        # Get all drafts for this customer
        drafts_response = supabase.table("drafts").select("*").eq("type", customer_type).eq("customer_name", customer_name).order("created_at", desc=True).execute()
        drafts = drafts_response.data if drafts_response.data else []

        # Merge all fields from all sources (most recent non-empty value wins)
        merged_details = {"customer_name": customer_name}

        # Process invoices first (older data)
        for invoice in reversed(invoices):
            for key, value in (invoice or {}).items():
                if value and key not in merged_details:
                    merged_details[key] = value

        # Process drafts second (newer data, takes precedence)
        for draft in reversed(drafts):
            for key, value in (draft or {}).items():
                if value and key not in merged_details:
                    merged_details[key] = value

        return merged_details if len(merged_details) > 1 else {}
    except Exception as e:
        print(f"Error getting customer details: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# STOCK MANAGEMENT ENDPOINTS
# ============================================================================

@app.get("/api/stock")
async def get_all_stock_summary():
    """Get stock summary for all products - with caching and batch queries"""
    try:
        current_time = time.time()
        # Return cached data if still fresh
        if _stock_cache["data"] is not None and (current_time - _stock_cache["timestamp"]) < STOCK_CACHE_TTL:
            return _stock_cache["data"]

        # Fetch fresh data using fast batch queries
        stock_summary = await get_stock_summary_fast()

        # Cache the result
        _stock_cache["data"] = stock_summary
        _stock_cache["timestamp"] = current_time
        return stock_summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stock/{product_id}")
async def get_product_current_stock(product_id: str):
    """Get current stock for product"""
    try:
        product = await get_product_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        stock = await get_product_stock(product_id)
        return {"product_id": product_id, "product_name": product["name"], "current_stock": stock}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# INVOICE NUMBER GENERATION
# ============================================================================

@app.get("/api/next-invoice-number/{invoice_type}")
async def get_next_invoice_number(invoice_type: str):
    """Generate next invoice number based on type"""
    try:
        if invoice_type == "purchase":
            # Get count of purchase invoices
            invoices = await get_purchase_invoices()
            count = len(invoices) + 1
            return {"invoice_number": f"PU-{datetime.now().strftime('%Y%m%d')}-{str(count).zfill(4)}"}
        elif invoice_type == "retail":
            # Get count of retail invoices
            invoices = await get_invoices()
            retail_count = sum(1 for inv in invoices if inv.get('type') == 'retail')
            count = retail_count + 1
            return {"invoice_number": f"GSCR-{datetime.now().year}-{str(count).zfill(4)}"}
        elif invoice_type == "patient":
            # Get count of patient invoices
            invoices = await get_invoices()
            patient_count = sum(1 for inv in invoices if inv.get('type') == 'patient')
            count = patient_count + 1
            return {"invoice_number": f"GCPC-{datetime.now().year}-{str(count).zfill(4)}"}
        else:
            raise HTTPException(status_code=400, detail=f"Unknown invoice type: {invoice_type}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# DASHBOARD ENDPOINTS
# ============================================================================

@app.get("/api/dashboard")
async def get_dashboard():
    """Get dashboard statistics"""
    try:
        stats = await get_dashboard_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# EXPIRY TRACKING ENDPOINTS
# ============================================================================

@app.get("/api/expiry")
async def get_expiry_data():
    """Get medicines expiring soon (within 90 days)"""
    try:
        expiring_items = await get_expiring_items(days_ahead=90)
        return expiring_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/expiry/debug")
async def get_expiry_debug():
    """Debug endpoint to check expiry data"""
    try:
        from .supabase_client import supabase

        # Get raw purchase items
        purchase_response = supabase.table("purchase_items").select("*").limit(10).execute()
        purchase_items = purchase_response.data if purchase_response.data else []

        # Get invoice items for this sample
        invoice_response = supabase.table("invoice_items").select("*").limit(10).execute()
        invoice_items = invoice_response.data if invoice_response.data else []

        # Get products for this sample
        products = await get_products()

        return {
            "purchase_items_count": len(purchase_items),
            "purchase_items_sample": purchase_items[:5],
            "invoice_items_count": len(invoice_items),
            "products_count": len(products),
            "expiring_items": await get_expiring_items(days_ahead=90)
        }
    except Exception as e:
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc()}

# ============================================================================
# SALES ENDPOINTS
# ============================================================================

@app.get("/api/sales")
async def get_all_sales():
    """Get all sales records"""
    try:
        sales = await get_sales()
        return sales
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/sales")
async def create_new_sale(sale: SalesModel):
    """Record a new sale"""
    try:
        sale_data = {
            "customer_name": sale.customer_name,
            "customer_phone": sale.customer_phone,
            "product_id": sale.product_id,
            "quantity": sale.quantity,
            "selling_price": sale.selling_price,
            "sale_date": sale.sale_date,
            "notes": sale.notes
        }
        new_sale = await create_sale(sale_data)
        if not new_sale:
            raise HTTPException(status_code=500, detail="Failed to create sale")
        return new_sale
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# EXPORT TO GOOGLE SHEETS
# ============================================================================

@app.get("/api/export/google-sheets")
async def export_to_google_sheets():
    """Export all database tables to existing Google Sheet"""
    try:
        from backend.google_sheets_client import add_sheet, write_data_to_sheet, get_spreadsheet_url

        # Existing spreadsheet ID - update this with your sheet ID
        spreadsheet_id = "1ddHcuKy2bSZZTNyUChep_CugvcP6C4TX6_DDho_yLAk"

        # Fetch all tables
        vendors = await get_vendors()
        products = await get_products()
        customers = await get_customers()
        invoices = await get_invoices()
        drafts = await get_drafts()
        purchase_invoices = await get_purchase_invoices()
        stock_ledger = await get_stock_ledger()

        # Prepare data for export
        tables_data = {
            'Vendors': vendors or [],
            'Products': products or [],
            'Customers': customers or [],
            'Invoices': invoices or [],
            'Drafts': drafts or [],
            'Purchase Invoices': purchase_invoices or [],
            'Stock Ledger': stock_ledger or []
        }

        # Create sheets and populate data
        for table_name, data in tables_data.items():
            try:
                add_sheet(spreadsheet_id, table_name)
                if data:
                    write_data_to_sheet(spreadsheet_id, table_name, data)
                    print(f"✓ {table_name}: {len(data)} records")
                else:
                    print(f"⚠ {table_name}: No data")
            except Exception as e:
                print(f"Error with {table_name}: {e}")
                continue

        return {
            "status": "success",
            "message": "All tables exported to Google Sheet",
            "spreadsheet_id": spreadsheet_id,
            "url": get_spreadsheet_url(spreadsheet_id),
            "sheet_count": len(tables_data)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

# ============================================================================
# STATIC FILES
# ============================================================================

@app.get("/")
async def serve_index():
    """Serve graftcare.html"""
    return FileResponse(Path(__file__).parent.parent / "graftcare.html")

@app.get("/main.js")
async def serve_main_js():
    """Serve main.js"""
    return FileResponse(Path(__file__).parent.parent / "main.js", media_type="application/javascript")

@app.get("/main.css")
async def serve_main_css():
    """Serve main.css"""
    return FileResponse(Path(__file__).parent.parent / "main.css", media_type="text/css")

@app.get("/states.js")
async def serve_states_js():
    """Serve states.js"""
    return FileResponse(Path(__file__).parent.parent / "states.js", media_type="application/javascript")
