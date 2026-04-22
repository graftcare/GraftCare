"""
Additional Retrieval and Search Endpoints for Graftcare
Add these to your main.py for advanced data retrieval
"""

from fastapi import FastAPI, HTTPException
from typing import Optional
from datetime import datetime

# These are helper functions to add to main.py

# ============================================================================
# ADVANCED RETRIEVAL - VENDORS
# ============================================================================

async def search_vendors(search_term: str = None):
    """Search vendors by name, GSTIN, or phone"""
    try:
        vendors = await get_vendors()

        if not search_term:
            return vendors

        search_term = search_term.lower()
        return [
            v for v in vendors
            if search_term in str(v.get("name", "")).lower()
            or search_term in str(v.get("gstin", "")).lower()
            or search_term in str(v.get("phone", "")).lower()
        ]
    except Exception as e:
        return []

@app.get("/api/vendors/search/{search_term}")
async def search_vendors_endpoint(search_term: str):
    """Search vendors by name, GSTIN, or phone"""
    try:
        results = await search_vendors(search_term)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ADVANCED RETRIEVAL - PRODUCTS
# ============================================================================

async def search_products(search_term: str = None, company: str = None):
    """Search products by name or company"""
    try:
        products = await get_products()

        results = products

        if search_term:
            search_term = search_term.lower()
            results = [
                p for p in results
                if search_term in str(p.get("name", "")).lower()
                or search_term in str(p.get("hsn_code", "")).lower()
            ]

        if company:
            results = [p for p in results if p.get("company", "").lower() == company.lower()]

        return results
    except Exception as e:
        return []

@app.get("/api/products/search/{search_term}")
async def search_products_endpoint(search_term: str, company: str = None):
    """Search products by name or HSN code"""
    try:
        results = await search_products(search_term, company)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/products/company/{company}")
async def get_products_by_company(company: str):
    """Get all products from a specific company"""
    try:
        results = await search_products(company=company)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ADVANCED RETRIEVAL - CUSTOMERS
# ============================================================================

async def search_customers(search_term: str = None):
    """Search customers by name, GSTIN, or phone"""
    try:
        customers = await get_customers()

        if not search_term:
            return customers

        search_term = search_term.lower()
        return [
            c for c in customers
            if search_term in str(c.get("name", "")).lower()
            or search_term in str(c.get("gstin", "")).lower()
            or search_term in str(c.get("phone", "")).lower()
        ]
    except Exception as e:
        return []

@app.get("/api/customers/search/{search_term}")
async def search_customers_endpoint(search_term: str):
    """Search customers by name, GSTIN, or phone"""
    try:
        results = await search_customers(search_term)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ADVANCED RETRIEVAL - PURCHASE INVOICES
# ============================================================================

@app.get("/api/purchase-invoices/vendor/{vendor_id}")
async def get_vendor_purchase_invoices(vendor_id: str):
    """Get all purchase invoices for a vendor"""
    try:
        invoices = await get_purchase_invoices()
        vendor_invoices = [inv for inv in invoices if inv["vendor_id"] == vendor_id]

        # Add items for each invoice
        for invoice in vendor_invoices:
            items = await get_purchase_items(invoice["id"])
            invoice["items"] = items

        return vendor_invoices
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/purchase-invoices/status/{status}")
async def get_purchase_invoices_by_status(status: str):
    """Get purchase invoices by payment status (pending, partial, paid)"""
    try:
        invoices = await get_purchase_invoices()
        filtered = [inv for inv in invoices if inv.get("payment_status") == status]

        for invoice in filtered:
            items = await get_purchase_items(invoice["id"])
            invoice["items"] = items

        return filtered
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/purchase-invoices/date-range")
async def get_purchase_invoices_by_date_range(from_date: str, to_date: str):
    """Get purchase invoices within date range (YYYY-MM-DD)"""
    try:
        invoices = await get_purchase_invoices()

        filtered = [
            inv for inv in invoices
            if from_date <= inv.get("invoice_date", "") <= to_date
        ]

        for invoice in filtered:
            items = await get_purchase_items(invoice["id"])
            invoice["items"] = items

        return filtered
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ADVANCED RETRIEVAL - SALES
# ============================================================================

@app.get("/api/sales/customer/{customer_id}")
async def get_customer_sales(customer_id: str):
    """Get all sales for a customer"""
    try:
        sales = await get_sales()
        customer_sales = [s for s in sales if s["customer_id"] == customer_id]

        for sale in customer_sales:
            items = await get_sales_items(sale["id"])
            sale["items"] = items

        return customer_sales
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sales/status/{status}")
async def get_sales_by_status(status: str):
    """Get sales by status (draft, proforma, final)"""
    try:
        sales = await get_sales()
        filtered = [s for s in sales if s.get("status") == status]

        for sale in filtered:
            items = await get_sales_items(sale["id"])
            sale["items"] = items

        return filtered
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sales/date-range")
async def get_sales_by_date_range(from_date: str, to_date: str):
    """Get sales within date range (YYYY-MM-DD)"""
    try:
        sales = await get_sales()

        filtered = [
            s for s in sales
            if from_date <= (s.get("invoice_date") or "") <= to_date
        ]

        for sale in filtered:
            items = await get_sales_items(sale["id"])
            sale["items"] = items

        return filtered
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ADVANCED RETRIEVAL - STOCK & INVENTORY
# ============================================================================

@app.get("/api/stock/low-stock")
async def get_low_stock(threshold: int = 10):
    """Get products with stock below threshold"""
    try:
        products = await get_products()
        low_stock = []

        for product in products:
            stock = await get_product_stock(product["id"])
            if stock < threshold:
                low_stock.append({
                    "product_id": product["id"],
                    "product_name": product["name"],
                    "company": product.get("company"),
                    "current_stock": stock,
                    "threshold": threshold
                })

        return low_stock
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stock/by-product/{product_id}")
async def get_product_stock_details(product_id: str):
    """Get detailed stock information for a product"""
    try:
        products = await get_products()
        product = next((p for p in products if p["id"] == product_id), None)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        current_stock = await get_product_stock(product_id)
        ledger = await get_stock_ledger(product_id)

        return {
            "product": product,
            "current_stock": current_stock,
            "ledger_entries": ledger,
            "total_purchased": sum([e["change_qty"] for e in ledger if e["reason"] == "purchase"]),
            "total_sold": abs(sum([e["change_qty"] for e in ledger if e["reason"] == "sale"])),
            "adjustments": sum([e["change_qty"] for e in ledger if e["reason"] == "adjustment"])
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# REPORTS & SUMMARIES
# ============================================================================

@app.get("/api/reports/vendor-summary")
async def get_vendor_summary():
    """Get summary of all vendors"""
    try:
        vendors = await get_vendors()
        invoices = await get_purchase_invoices()

        summary = []
        for vendor in vendors:
            vendor_invoices = [inv for inv in invoices if inv["vendor_id"] == vendor["id"]]
            total_amount = sum([inv.get("grand_total", 0) for inv in vendor_invoices])

            summary.append({
                "vendor_id": vendor["id"],
                "name": vendor["name"],
                "gstin": vendor["gstin"],
                "phone": vendor["phone"],
                "city": vendor.get("city"),
                "total_invoices": len(vendor_invoices),
                "total_amount": round(total_amount, 2),
                "avg_invoice": round(total_amount / len(vendor_invoices), 2) if vendor_invoices else 0
            })

        return sorted(summary, key=lambda x: x["total_amount"], reverse=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reports/customer-summary")
async def get_customer_summary():
    """Get summary of all customers"""
    try:
        customers = await get_customers()
        sales = await get_sales()

        summary = []
        for customer in customers:
            customer_sales = [s for s in sales if s["customer_id"] == customer["id"]]
            total_amount = sum([s.get("grand_total", 0) for s in customer_sales])

            summary.append({
                "customer_id": customer["id"],
                "name": customer["name"],
                "gstin": customer.get("gstin"),
                "phone": customer["phone"],
                "city": customer.get("city"),
                "total_sales": len(customer_sales),
                "total_amount": round(total_amount, 2),
                "outstanding_balance": customer.get("outstanding_balance", 0),
                "credit_limit": customer.get("credit_limit", 0)
            })

        return sorted(summary, key=lambda x: x["total_amount"], reverse=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reports/sales-summary")
async def get_sales_summary():
    """Get sales summary by status"""
    try:
        sales = await get_sales()

        draft_count = len([s for s in sales if s.get("status") == "draft"])
        proforma_count = len([s for s in sales if s.get("status") == "proforma"])
        final_count = len([s for s in sales if s.get("status") == "final"])

        draft_amount = sum([s.get("grand_total", 0) for s in sales if s.get("status") == "draft"])
        proforma_amount = sum([s.get("grand_total", 0) for s in sales if s.get("status") == "proforma"])
        final_amount = sum([s.get("grand_total", 0) for s in sales if s.get("status") == "final"])

        return {
            "draft": {"count": draft_count, "amount": round(draft_amount, 2)},
            "proforma": {"count": proforma_count, "amount": round(proforma_amount, 2)},
            "final": {"count": final_count, "amount": round(final_amount, 2)},
            "total": {
                "count": draft_count + proforma_count + final_count,
                "amount": round(draft_amount + proforma_amount + final_amount, 2)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reports/purchase-summary")
async def get_purchase_summary():
    """Get purchase summary"""
    try:
        invoices = await get_purchase_invoices()

        pending = len([i for i in invoices if i.get("payment_status") == "pending"])
        partial = len([i for i in invoices if i.get("payment_status") == "partial"])
        paid = len([i for i in invoices if i.get("payment_status") == "paid"])

        pending_amount = sum([i.get("grand_total", 0) for i in invoices if i.get("payment_status") == "pending"])
        partial_amount = sum([i.get("grand_total", 0) for i in invoices if i.get("payment_status") == "partial"])
        paid_amount = sum([i.get("grand_total", 0) for i in invoices if i.get("payment_status") == "paid"])

        return {
            "pending": {"count": pending, "amount": round(pending_amount, 2)},
            "partial": {"count": partial, "amount": round(partial_amount, 2)},
            "paid": {"count": paid, "amount": round(paid_amount, 2)},
            "total": {
                "count": pending + partial + paid,
                "amount": round(pending_amount + partial_amount + paid_amount, 2)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# EXPORT ENDPOINTS (for downloading data)
# ============================================================================

@app.get("/api/export/vendors")
async def export_vendors():
    """Export all vendors data"""
    try:
        vendors = await get_vendors()
        return {
            "export_type": "vendors",
            "exported_at": datetime.now().isoformat(),
            "total_records": len(vendors),
            "data": vendors
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/export/products")
async def export_products():
    """Export all products data"""
    try:
        products = await get_products()
        return {
            "export_type": "products",
            "exported_at": datetime.now().isoformat(),
            "total_records": len(products),
            "data": products
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/export/purchase-invoices")
async def export_purchase_invoices():
    """Export all purchase invoices"""
    try:
        invoices = await get_purchase_invoices()

        for invoice in invoices:
            items = await get_purchase_items(invoice["id"])
            invoice["items"] = items

        return {
            "export_type": "purchase_invoices",
            "exported_at": datetime.now().isoformat(),
            "total_records": len(invoices),
            "data": invoices
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/export/sales")
async def export_sales():
    """Export all sales"""
    try:
        sales = await get_sales()

        for sale in sales:
            items = await get_sales_items(sale["id"])
            sale["items"] = items

        return {
            "export_type": "sales",
            "exported_at": datetime.now().isoformat(),
            "total_records": len(sales),
            "data": sales
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
