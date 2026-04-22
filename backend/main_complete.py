"""
Complete Supabase Integration for Graftcare
All endpoints connected to Supabase database
UI → FastAPI → Supabase flow
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import json
from pathlib import Path
from datetime import datetime
import os
from dotenv import load_dotenv
import uuid

# Import Supabase client and functions
from supabase_client import (
    get_vendors, create_vendor, update_vendor, delete_vendor, get_vendor_by_gstin, get_vendor_by_phone,
    get_products, create_product, update_product, delete_product,
    get_customers, create_customer, update_customer, delete_customer,
    get_purchase_invoices, create_purchase_invoice, update_purchase_invoice, delete_purchase_invoice,
    get_purchase_items, create_purchase_items, delete_purchase_items,
    get_sales, create_sale, update_sale, delete_sale,
    get_sales_items, create_sales_items, delete_sales_items,
    get_stock_ledger, add_stock_ledger_entry, get_product_stock, supabase
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

class CustomerModel(BaseModel):
    id: Optional[str] = None
    name: str
    contact_person: Optional[str] = None
    phone: str
    gstin: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None
    credit_limit: float = 0.0
    outstanding_balance: float = 0.0

class PurchaseInvoiceModel(BaseModel):
    id: Optional[str] = None
    vendor_id: str
    vendor_invoice_no: str
    invoice_date: str
    payment_mode: Optional[str] = None
    amount_paid: Optional[float] = None
    paid_by: Optional[str] = None
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

class SaleModel(BaseModel):
    id: Optional[str] = None
    customer_id: str
    status: str = "draft"
    invoice_date: Optional[str] = None
    subtotal: Optional[float] = None
    total_gst: Optional[float] = None
    discount_amount: Optional[float] = None
    grand_total: Optional[float] = None
    payment_mode: Optional[str] = None
    amount_received: Optional[float] = None
    notes: Optional[str] = None
    items: List[Dict[str, Any]] = []

class DraftInvoiceModel(BaseModel):
    id: Optional[str] = None
    data: dict
    created_date: Optional[str] = None
    updated_date: Optional[str] = None

# ============================================================================
# VENDORS
# ============================================================================

@app.get("/api/vendors")
async def get_all_vendors():
    """Get all vendors"""
    try:
        vendors = await get_vendors()
        return vendors
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/vendors")
async def create_new_vendor(vendor: VendorModel):
    """Create new vendor"""
    try:
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

        result = await create_vendor(vendor.dict(exclude_none=True))
        return {"id": result["id"], "message": "Vendor created"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/vendors/{vendor_id}")
async def update_existing_vendor(vendor_id: str, vendor: VendorModel):
    """Update vendor"""
    try:
        # Check phone uniqueness
        if vendor.phone:
            existing = await get_vendor_by_phone(vendor.phone)
            if existing and existing["id"] != vendor_id:
                raise HTTPException(status_code=400, detail="Phone already used")

        # Check GSTIN uniqueness
        if vendor.gstin:
            existing = await get_vendor_by_gstin(vendor.gstin)
            if existing and existing["id"] != vendor_id:
                raise HTTPException(status_code=400, detail="GSTIN already used")

        result = await update_vendor(vendor_id, vendor.dict(exclude_none=True))
        if not result:
            raise HTTPException(status_code=404, detail="Vendor not found")
        return {"message": "Vendor updated"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/vendors/{vendor_id}")
async def delete_existing_vendor(vendor_id: str):
    """Delete vendor"""
    try:
        result = await delete_vendor(vendor_id)
        return {"message": "Vendor deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/vendors/{vendor_id}/details")
async def get_vendor_details(vendor_id: str):
    """Get vendor with purchase history"""
    try:
        # Get vendor
        vendors = await get_vendors()
        vendor = next((v for v in vendors if v["id"] == vendor_id), None)
        if not vendor:
            raise HTTPException(status_code=404, detail="Vendor not found")

        # Get vendor's invoices
        invoices = await get_purchase_invoices()
        vendor_invoices = [inv for inv in invoices if inv["vendor_id"] == vendor_id]

        # Get items for each invoice
        vendor_purchases = []
        for inv in vendor_invoices:
            items = await get_purchase_items(inv["id"])
            vendor_purchases.append({
                "id": inv["id"],
                "invoice_no": inv["vendor_invoice_no"],
                "invoice_date": inv["invoice_date"],
                "amount": inv["grand_total"],
                "items": items
            })

        return {
            "id": vendor["id"],
            "name": vendor["name"],
            "contact_person": vendor.get("contact_person"),
            "phone": vendor["phone"],
            "gstin": vendor["gstin"],
            "address": vendor.get("address"),
            "city": vendor.get("city"),
            "pincode": vendor.get("pincode"),
            "bank_name": vendor.get("bank_name"),
            "bank_acc": vendor.get("bank_acc"),
            "bank_ifsc": vendor.get("bank_ifsc"),
            "purchases": vendor_purchases,
            "total_purchases": len(vendor_purchases),
            "total_amount": sum([p["amount"] for p in vendor_purchases])
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# PRODUCTS
# ============================================================================

@app.get("/api/products")
async def get_all_products():
    """Get all products"""
    try:
        products = await get_products()
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/products")
async def create_new_product(product: ProductModel):
    """Create new product"""
    try:
        if product.cost_price > product.mrp:
            raise HTTPException(status_code=400, detail=f"Cost price cannot exceed MRP")

        result = await create_product(product.dict(exclude_none=True))
        return {"id": result["id"], "message": "Product created"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/products/{product_id}")
async def update_existing_product(product_id: str, product: ProductModel):
    """Update product"""
    try:
        if product.cost_price > product.mrp:
            raise HTTPException(status_code=400, detail="Cost price cannot exceed MRP")

        result = await update_product(product_id, product.dict(exclude_none=True))
        if not result:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"message": "Product updated"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/products/{product_id}")
async def delete_existing_product(product_id: str):
    """Delete product"""
    try:
        result = await delete_product(product_id)
        return {"message": "Product deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# CUSTOMERS
# ============================================================================

@app.get("/api/customers")
async def get_all_customers():
    """Get all customers"""
    try:
        customers = await get_customers()
        return customers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/customers")
async def create_new_customer(customer: CustomerModel):
    """Create new customer"""
    try:
        result = await create_customer(customer.dict(exclude_none=True))
        return {"id": result["id"], "message": "Customer created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/customers/{customer_id}")
async def update_existing_customer(customer_id: str, customer: CustomerModel):
    """Update customer"""
    try:
        result = await update_customer(customer_id, customer.dict(exclude_none=True))
        if not result:
            raise HTTPException(status_code=404, detail="Customer not found")
        return {"message": "Customer updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/customers/{customer_id}")
async def delete_existing_customer(customer_id: str):
    """Delete customer"""
    try:
        result = await delete_customer(customer_id)
        return {"message": "Customer deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# PURCHASE INVOICES
# ============================================================================

@app.get("/api/purchase-invoices")
async def get_all_purchase_invoices():
    """Get all purchase invoices with items"""
    try:
        invoices = await get_purchase_invoices()
        for invoice in invoices:
            items = await get_purchase_items(invoice["id"])
            invoice["items"] = items
        return invoices
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/purchase-invoices")
async def create_new_purchase_invoice(invoice: PurchaseInvoiceModel):
    """Create new purchase invoice with items"""
    try:
        items = invoice.items
        invoice_data = invoice.dict(exclude={"items"}, exclude_none=True)

        # Check for duplicate invoice number per vendor
        all_invoices = await get_purchase_invoices()
        duplicate = next(
            (inv for inv in all_invoices
             if inv["vendor_id"] == invoice.vendor_id and inv["vendor_invoice_no"] == invoice.vendor_invoice_no),
            None
        )
        if duplicate:
            raise HTTPException(status_code=400, detail="Invoice number already exists for this vendor")

        # Create invoice
        result = await create_purchase_invoice(invoice_data)
        invoice_id = result["id"]

        # Create items
        if items:
            items_data = []
            for item in items:
                item["purchase_invoice_id"] = invoice_id
                items_data.append(item)

            await create_purchase_items(items_data)

            # Add stock ledger entries
            for item in items:
                await add_stock_ledger_entry({
                    "product_id": item["product_id"],
                    "change_qty": item["qty"],
                    "reason": "purchase",
                    "reference_id": invoice_id,
                    "notes": f"Batch: {item.get('batch', '')}, Expiry: {item.get('expiry', '')}"
                })

        return {"id": invoice_id, "message": "Purchase invoice created with stock entries"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/purchase-invoices/{invoice_id}")
async def update_existing_purchase_invoice(invoice_id: str, invoice: PurchaseInvoiceModel):
    """Update purchase invoice"""
    try:
        items = invoice.items
        invoice_data = invoice.dict(exclude={"items"}, exclude_none=True)

        # Update invoice
        result = await update_purchase_invoice(invoice_id, invoice_data)
        if not result:
            raise HTTPException(status_code=404, detail="Invoice not found")

        # Update items
        if items is not None:
            await delete_purchase_items(invoice_id)
            if items:
                items_data = []
                for item in items:
                    item["purchase_invoice_id"] = invoice_id
                    items_data.append(item)
                await create_purchase_items(items_data)

        return {"message": "Purchase invoice updated"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/purchase-invoices/{invoice_id}")
async def delete_existing_purchase_invoice(invoice_id: str):
    """Delete purchase invoice and items"""
    try:
        await delete_purchase_items(invoice_id)
        result = await delete_purchase_invoice(invoice_id)
        return {"message": "Purchase invoice deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# SALES
# ============================================================================

@app.get("/api/sales")
async def get_all_sales():
    """Get all sales with items"""
    try:
        sales = await get_sales()
        for sale in sales:
            items = await get_sales_items(sale["id"])
            sale["items"] = items
        return sales
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/sales")
async def create_new_sale(sale: SaleModel):
    """Create new sale with items"""
    try:
        items = sale.items
        sale_data = sale.dict(exclude={"items"}, exclude_none=True)

        # Create sale
        result = await create_sale(sale_data)
        sale_id = result["id"]

        # Create items
        if items:
            items_data = []
            for item in items:
                item["sale_id"] = sale_id
                items_data.append(item)
            await create_sales_items(items_data)

            # Add stock ledger entries
            for item in items:
                await add_stock_ledger_entry({
                    "product_id": item["product_id"],
                    "change_qty": -item["qty"],  # Negative for sales
                    "reason": "sale",
                    "reference_id": sale_id,
                    "notes": f"Batch: {item.get('batch', '')}"
                })

        return {
            "id": sale_id,
            "invoice_number": result.get("invoice_number", ""),
            "message": "Sale created"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/sales/{sale_id}")
async def update_existing_sale(sale_id: str, sale: SaleModel):
    """Update sale"""
    try:
        items = sale.items
        sale_data = sale.dict(exclude={"items"}, exclude_none=True)

        result = await update_sale(sale_id, sale_data)
        if not result:
            raise HTTPException(status_code=404, detail="Sale not found")

        # Update items
        if items is not None:
            await delete_sales_items(sale_id)
            if items:
                items_data = []
                for item in items:
                    item["sale_id"] = sale_id
                    items_data.append(item)
                await create_sales_items(items_data)

        return {"message": "Sale updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/sales/{sale_id}")
async def delete_existing_sale(sale_id: str):
    """Delete sale and items"""
    try:
        await delete_sales_items(sale_id)
        result = await delete_sale(sale_id)
        return {"message": "Sale deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/sales/{sale_id}/finalize")
async def finalize_sale(sale_id: str):
    """Finalize sale"""
    try:
        all_sales = await get_sales()
        sale = next((s for s in all_sales if s["id"] == sale_id), None)
        if not sale:
            raise HTTPException(status_code=404, detail="Sale not found")

        if sale["status"] == "final":
            raise HTTPException(status_code=400, detail="Sale already finalized")

        # Update status to final
        await update_sale(sale_id, {"status": "final"})

        return {
            "invoice_id": sale_id,
            "invoice_number": sale.get("invoice_number", ""),
            "message": "Sale finalized"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# STOCK
# ============================================================================

@app.get("/api/stock")
async def get_all_stock():
    """Get stock for all products"""
    try:
        products = await get_products()
        stock_data = []

        for product in products:
            stock = await get_product_stock(product["id"])
            stock_data.append({
                "product_id": product["id"],
                "product_name": product["name"],
                "hsn_code": product.get("hsn_code", ""),
                "pack": product.get("pack", ""),
                "company": product.get("company", ""),
                "cost_price": product.get("cost_price", 0),
                "mrp": product.get("mrp", 0),
                "gst_rate": product.get("gst_rate", 0),
                "available": stock
            })

        return stock_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stock/{product_id}")
async def get_product_current_stock(product_id: str):
    """Get current stock for a product"""
    try:
        stock = await get_product_stock(product_id)
        return {"product_id": product_id, "stock": stock}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stock/ledger/{product_id}")
async def get_product_stock_ledger(product_id: str):
    """Get stock ledger for a product"""
    try:
        ledger = await get_stock_ledger(product_id)
        return ledger
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# DASHBOARD
# ============================================================================

@app.get("/api/dashboard")
async def get_dashboard():
    """Get dashboard summary"""
    try:
        vendors = await get_vendors()
        products = await get_products()
        invoices = await get_purchase_invoices()
        sales = await get_sales()

        total_vendors = len(vendors)
        total_products = len(products)
        total_purchases = sum([inv.get("grand_total", 0) for inv in invoices])
        total_sales = sum([s.get("grand_total", 0) for s in sales if s.get("status") == "final"])

        return {
            "total_vendors": total_vendors,
            "total_products": total_products,
            "total_purchases": round(total_purchases, 2),
            "total_sales": round(total_sales, 2),
            "total_invoices": len(invoices),
            "total_sales_orders": len(sales)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# HEALTH & ROOT
# ============================================================================

@app.get("/api/health")
async def health():
    """Health check"""
    return {"status": "running", "database": "supabase"}

@app.get("/")
async def root():
    """Serve the frontend HTML"""
    html_file = Path(__file__).parent.parent / "graftcare.html"
    if html_file.exists():
        return FileResponse(html_file, media_type="text/html")
    return {"message": "Graft Care Pharma API"}

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
