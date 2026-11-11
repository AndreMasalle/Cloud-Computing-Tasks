from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict
import uuid
from datetime import datetime

app = FastAPI(title="E-Commerce Analytics System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ IN-MEMORY STORAGE ============
products_db: Dict[str, dict] = {}
customers_db: Dict[str, dict] = {}
orders_db: Dict[str, dict] = {}


# ============ SCHEMAS ============
class ProductIn(BaseModel):
    name: str
    category: str
    price: float
    stock: int


class CustomerIn(BaseModel):
    name: str
    email: str
    tier: str  # Bronze, Silver, Gold, Platinum


class OrderIn(BaseModel):
    customer_id: str
    product_id: str
    quantity: int


# ============ CRUD: PRODUCTS ============
@app.post("/api/products")
def create_product(payload: ProductIn):
    pid = str(uuid.uuid4())
    products_db[pid] = {"id": pid, **payload.dict()}
    return products_db[pid]


@app.get("/api/products")
def list_products():
    return list(products_db.values())


@app.put("/api/products/{pid}")
def update_product(pid: str, payload: ProductIn):
    if pid not in products_db:
        raise HTTPException(404, "Product not found")
    products_db[pid].update(payload.dict())
    return products_db[pid]


@app.delete("/api/products/{pid}")
def delete_product(pid: str):
    if pid not in products_db:
        raise HTTPException(404, "Product not found")
    del products_db[pid]
    return {"message": "deleted"}


# ============ CRUD: CUSTOMERS ============
@app.post("/api/customers")
def create_customer(payload: CustomerIn):
    cid = str(uuid.uuid4())
    customers_db[cid] = {"id": cid, **payload.dict()}
    return customers_db[cid]


@app.get("/api/customers")
def list_customers():
    return list(customers_db.values())


@app.put("/api/customers/{cid}")
def update_customer(cid: str, payload: CustomerIn):
    if cid not in customers_db:
        raise HTTPException(404, "Customer not found")
    customers_db[cid].update(payload.dict())
    return customers_db[cid]


@app.delete("/api/customers/{cid}")
def delete_customer(cid: str):
    if cid not in customers_db:
        raise HTTPException(404, "Customer not found")
    del customers_db[cid]
    return {"message": "deleted"}


# ============ CRUD: ORDERS (Multi-Entity) ============
@app.post("/api/orders")
def create_order(payload: OrderIn):
    if payload.customer_id not in customers_db:
        raise HTTPException(400, "Customer ID tidak valid")
    if payload.product_id not in products_db:
        raise HTTPException(400, "Product ID tidak valid")

    oid = str(uuid.uuid4())
    product = products_db[payload.product_id]
    total_price = product["price"] * payload.quantity

    orders_db[oid] = {
        "id": oid,
        **payload.dict(),
        "customer_name": customers_db[payload.customer_id]["name"],
        "product_name": product["name"],
        "total_price": total_price,
        "order_date": datetime.utcnow().isoformat()
    }
    return orders_db[oid]


@app.get("/api/orders")
def list_orders():
    return list(orders_db.values())


@app.put("/api/orders/{oid}")
def update_order(oid: str, payload: OrderIn):
    """Ubah pelanggan, produk, atau jumlah pesanan. Total dihitung ulang; tanggal pesanan tetap."""
    if oid not in orders_db:
        raise HTTPException(404, "Order not found")
    if payload.customer_id not in customers_db:
        raise HTTPException(400, "Customer ID tidak valid")
    if payload.product_id not in products_db:
        raise HTTPException(400, "Product ID tidak valid")
    if payload.quantity < 1:
        raise HTTPException(400, "Quantity minimal 1")

    product = products_db[payload.product_id]
    orders_db[oid].update({
        **payload.dict(),
        "customer_name": customers_db[payload.customer_id]["name"],
        "product_name": product["name"],
        "total_price": product["price"] * payload.quantity,
    })
    return orders_db[oid]


@app.delete("/api/orders/{oid}")
def delete_order(oid: str):
    if oid not in orders_db:
        raise HTTPException(404, "Order not found")
    del orders_db[oid]
    return {"message": "deleted"}


# ============ FITUR MULTI-ENTITY (ANALYTICS) ============
@app.get("/api/analytics/top-customers")
def top_customers():
    """Menghitung total belanja tiap pelanggan (Order + Customer)"""
    agg = {}
    for order in orders_db.values():
        cid = order["customer_id"]
        agg.setdefault(cid, {"customer_id": cid, "customer_name": order["customer_name"], "total_spent": 0})
        agg[cid]["total_spent"] += order["total_price"]

    result = sorted(agg.values(), key=lambda x: x["total_spent"], reverse=True)
    return result


@app.get("/api/analytics/top-products")
def top_products():
    """Menghitung total pendapatan dan kuantitas terjual per produk (Order + Product)"""
    agg = {}
    for order in orders_db.values():
        pid = order["product_id"]
        agg.setdefault(pid,
                       {"product_id": pid, "product_name": order["product_name"], "total_revenue": 0, "items_sold": 0})
        agg[pid]["total_revenue"] += order["total_price"]
        agg[pid]["items_sold"] += order["quantity"]

    result = sorted(agg.values(), key=lambda x: x["total_revenue"], reverse=True)
    return result


@app.get("/api/dashboard")
def dashboard():
    total_revenue = sum(o["total_price"] for o in orders_db.values())
    return {
        "total_products": len(products_db),
        "total_customers": len(customers_db),
        "total_orders": len(orders_db),
        "total_revenue": total_revenue,
        "recent_orders": sorted(orders_db.values(), key=lambda x: x["order_date"], reverse=True)[:5]
    }