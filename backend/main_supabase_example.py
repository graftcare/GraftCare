# ============================================================================
# EXAMPLE: Converting FastAPI routes from Excel to Supabase
# This shows how to replace your existing routes with Supabase operations
# ============================================================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

# Import your Supabase client functions
from supabase_client import (
    get_vendors, create_vendor, update_vendor, delete_vendor, get_vendor_by_gstin, get_vendor_by_phone,
    get_products, create_product, update_product, delete_product,
    get_customers, create_customer, update_customer, delete_customer,
    get_purchase_invoices, create_purchase_invoice, update_purchase_invoice, delete_purchase_invoice,
    get_purchase_items, create_purchase_items, delete_purchase_items,
    get_sales, create_sale, update_sale, delete_sale,
    get_sales_items, create_sales_items, delete_sales_items,
    get_stock_ledger, add_stock_ledger_entry, get_product_stock
)

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# PYDANTIC MODELS (keep as-is from your current main.py)
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


# ============================================================================
# VENDORS - SUPABASE ROUTES
# ============================================================================

@app.get("/api/vendors")
async def get_all_vendors():
    """Get all vendors from Supabase"""
    vendors = await get_vendors()
    return vendors

@app.post("/api/vendors")
async def create_new_vendor(vendor: VendorModel):
    """Create new vendor in Supabase"""
    # Check for duplicate phone
    if vendor.phone:
        existing = await get_vendor_by_phone(vendor.phone)
        if existing:
            raise HTTPException(status_code=400, detail="Phone already exists")

    # Check for duplicate GSTIN
    if vendor.gstin:
        existing = await get_vendor_by_gstin(vendor.gstin)
        if existing:
            raise HTTPException(status_code=400, detail="GSTIN already exists")

    # Create vendor (Supabase will generate UUID for id if not provided)
    result = await create_vendor(vendor.dict(exclude_none=True))
    return {"id": result["id"], "message": "Vendor created"}

@app.put("/api/vendors/{vendor_id}")
async def update_existing_vendor(vendor_id: str, vendor: VendorModel):
    """Update vendor in Supabase"""
    # Check phone uniqueness (excluding current vendor)
    if vendor.phone:
        existing = await get_vendor_by_phone(vendor.phone)
        if existing and existing["id"] != vendor_id:
            raise HTTPException(status_code=400, detail="Phone already used by another vendor")

    # Check GSTIN uniqueness (excluding current vendor)
    if vendor.gstin:
        existing = await get_vendor_by_gstin(vendor.gstin)
        if existing and existing["id"] != vendor_id:
            raise HTTPException(status_code=400, detail="GSTIN already used by another vendor")

    result = await update_vendor(vendor_id, vendor.dict(exclude_none=True))
    if not result:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return {"message": "Vendor updated"}

@app.delete("/api/vendors/{vendor_id}")
async def delete_existing_vendor(vendor_id: str):
    """Delete vendor from Supabase"""
    result = await delete_vendor(vendor_id)
    return {"message": "Vendor deleted"}


# ============================================================================
# PRODUCTS - SUPABASE ROUTES
# ============================================================================

@app.get("/api/products")
async def get_all_products():
    """Get all products from Supabase"""
    products = await get_products()
    return products

@app.post("/api/products")
async def create_new_product(product: ProductModel):
    """Create new product in Supabase"""
    # Validation: cost_price <= mrp
    if product.cost_price > product.mrp:
        raise HTTPException(status_code=400, detail=f"Cost price (₹{product.cost_price}) cannot exceed MRP (₹{product.mrp})")

    result = await create_product(product.dict(exclude_none=True))
    return {"id": result["id"], "message": "Product created"}

@app.put("/api/products/{product_id}")
async def update_existing_product(product_id: str, product: ProductModel):
    """Update product in Supabase"""
    if product.cost_price > product.mrp:
        raise HTTPException(status_code=400, detail=f"Cost price cannot exceed MRP")

    result = await update_product(product_id, product.dict(exclude_none=True))
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product updated"}

@app.delete("/api/products/{product_id}")
async def delete_existing_product(product_id: str):
    """Delete product from Supabase"""
    result = await delete_product(product_id)
    return {"message": "Product deleted"}


# ============================================================================
# CUSTOMERS - SUPABASE ROUTES (NEW - for sales functionality)
# ============================================================================

@app.get("/api/customers")
async def get_all_customers():
    """Get all customers from Supabase"""
    customers = await get_customers()
    return customers

@app.post("/api/customers")
async def create_new_customer(customer_data: dict):
    """Create new customer in Supabase"""
    result = await create_customer(customer_data)
    return {"id": result["id"], "message": "Customer created"}

@app.put("/api/customers/{customer_id}")
async def update_existing_customer(customer_id: str, customer_data: dict):
    """Update customer in Supabase"""
    result = await update_customer(customer_id, customer_data)
    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer updated"}

@app.delete("/api/customers/{customer_id}")
async def delete_existing_customer(customer_id: str):
    """Delete customer from Supabase"""
    result = await delete_customer(customer_id)
    return {"message": "Customer deleted"}


# ============================================================================
# PURCHASE INVOICES - SUPABASE ROUTES
# ============================================================================

@app.get("/api/purchase-invoices")
async def get_all_purchase_invoices():
    """Get all purchase invoices with items"""
    invoices = await get_purchase_invoices()

    # For each invoice, fetch its items
    for invoice in invoices:
        items = await get_purchase_items(invoice["id"])
        invoice["items"] = items

    return invoices

@app.post("/api/purchase-invoices")
async def create_new_purchase_invoice(invoice_data: dict):
    """Create new purchase invoice with items"""
    items = invoice_data.pop("items", [])  # Extract items from request

    # Create invoice
    result = await create_purchase_invoice(invoice_data)
    invoice_id = result["id"]

    # Create items (if any)
    if items:
        for item in items:
            item["purchase_invoice_id"] = invoice_id
        await create_purchase_items(items)

        # Add stock ledger entries for each item purchased
        for item in items:
            await add_stock_ledger_entry({
                "product_id": item["product_id"],
                "change_qty": item["qty"],
                "reason": "purchase",
                "reference_id": invoice_id,
                "notes": f"Batch: {item.get('batch', '')}, Expiry: {item.get('expiry', '')}"
            })

    return {"id": invoice_id, "message": "Purchase invoice created with stock entries"}

@app.put("/api/purchase-invoices/{invoice_id}")
async def update_existing_purchase_invoice(invoice_id: str, invoice_data: dict):
    """Update purchase invoice"""
    items = invoice_data.pop("items", None)

    # Update invoice
    result = await update_purchase_invoice(invoice_id, invoice_data)
    if not result:
        raise HTTPException(status_code=404, detail="Invoice not found")

    # Update items if provided
    if items is not None:
        await delete_purchase_items(invoice_id)
        if items:
            for item in items:
                item["purchase_invoice_id"] = invoice_id
            await create_purchase_items(items)

    return {"message": "Purchase invoice updated"}

@app.delete("/api/purchase-invoices/{invoice_id}")
async def delete_existing_purchase_invoice(invoice_id: str):
    """Delete purchase invoice and its items"""
    # Delete items first (due to foreign key)
    await delete_purchase_items(invoice_id)

    # Delete invoice
    result = await delete_purchase_invoice(invoice_id)
    return {"message": "Purchase invoice deleted"}


# ============================================================================
# SALES - SUPABASE ROUTES
# ============================================================================

@app.get("/api/sales")
async def get_all_sales():
    """Get all sales with items"""
    sales = await get_sales()

    # For each sale, fetch its items
    for sale in sales:
        items = await get_sales_items(sale["id"])
        sale["items"] = items

    return sales

@app.post("/api/sales")
async def create_new_sale(sale_data: dict):
    """Create new sale with items"""
    items = sale_data.pop("items", [])

    # Create sale
    result = await create_sale(sale_data)
    sale_id = result["id"]

    # Create items (if any)
    if items:
        for item in items:
            item["sale_id"] = sale_id
        await create_sales_items(items)

    return {"id": sale_id, "message": "Sale created", "invoice_number": result.get("invoice_number")}

@app.delete("/api/sales/{sale_id}")
async def delete_existing_sale(sale_id: str):
    """Delete sale and restore stock"""
    # Delete items first
    await delete_sales_items(sale_id)

    # Delete sale
    result = await delete_sale(sale_id)

    # Could add logic here to restore stock if needed

    return {"message": "Sale deleted"}


# ============================================================================
# STOCK QUERIES
# ============================================================================

@app.get("/api/stock/{product_id}")
async def get_product_current_stock(product_id: str):
    """Get current stock level for a product"""
    stock = await get_product_stock(product_id)
    return {"product_id": product_id, "stock": stock}

@app.get("/api/stock")
async def get_all_stock():
    """Get stock for all products"""
    products = await get_products()
    stock_data = []

    for product in products:
        stock = await get_product_stock(product["id"])
        stock_data.append({
            "product_id": product["id"],
            "product_name": product["name"],
            "stock": stock
        })

    return stock_data


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
