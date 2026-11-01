"""catalog-service : produits, catégories et stock de QuickShop."""
import os
import socket
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from .data import seed_products

SERVICE = "catalog-service"
VERSION = "1.0.0"
STARTED_AT = datetime.now(timezone.utc)
LOW_STOCK = int(os.getenv("LOW_STOCK_THRESHOLD", "5"))

app = FastAPI(
    title="QuickShop · Catalog Service",
    version=VERSION,
    description="Microservice **catalogue** : produits, catégories et gestion du stock. "
    "Appelé par la gateway (lecture) et par order-service (réservation de stock).",
)

# Stockage en mémoire, propre à ce service (principe « une base par microservice »).
# Les endpoints sont async : ils s'exécutent dans une seule boucle, sans accès concurrent.
products = {p["id"]: p for p in seed_products()}


class Quantity(BaseModel):
    quantity: int = Field(gt=0, le=100)


class StockUpdate(BaseModel):
    stock: int = Field(ge=0, le=100000)


@app.exception_handler(HTTPException)
async def http_error(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": "Error", "message": exc.detail})


@app.exception_handler(RequestValidationError)
async def validation_error(request: Request, exc: RequestValidationError):
    first = exc.errors()[0] if exc.errors() else {}
    field = ".".join(str(x) for x in first.get("loc", []) if x != "body")
    return JSONResponse(status_code=400, content={"error": "Bad Request", "message": f"{field} : {first.get('msg', 'invalide')}"})


def public(p):
    return {**p, "lowStock": 0 < p["stock"] <= LOW_STOCK, "available": p["stock"] > 0}


def find(pid: int):
    p = products.get(pid)
    if p is None:
        raise HTTPException(status_code=404, detail=f"Produit {pid} introuvable")
    return p


@app.get("/health", tags=["Supervision"])
async def health():
    return {"status": "UP"}


@app.get("/info", tags=["Supervision"])
async def info():
    return {
        "service": SERVICE,
        "version": VERSION,
        "language": "Python · FastAPI",
        "hostname": socket.gethostname(),
        "startedAt": STARTED_AT.isoformat(),
        "uptimeSeconds": int((datetime.now(timezone.utc) - STARTED_AT).total_seconds()),
        "products": len(products),
        "unitsInStock": sum(p["stock"] for p in products.values()),
        "lowStockProducts": sum(1 for p in products.values() if 0 < p["stock"] <= LOW_STOCK),
    }


@app.get("/categories", tags=["Catalogue"])
async def categories():
    counts = {}
    for p in products.values():
        counts[p["category"]] = counts.get(p["category"], 0) + 1
    return [{"name": name, "count": count} for name, count in sorted(counts.items())]


@app.get("/products", tags=["Catalogue"])
async def list_products(category: str | None = None, q: str | None = None, lowStock: bool = False):
    result = list(products.values())
    if category:
        result = [p for p in result if p["category"].lower() == category.lower()]
    if q:
        needle = q.lower()
        result = [p for p in result if needle in p["name"].lower() or needle in p["description"].lower()]
    if lowStock:
        result = [p for p in result if p["stock"] <= LOW_STOCK]
    return [public(p) for p in result]


@app.get("/products/{pid}", tags=["Catalogue"])
async def get_product(pid: int):
    return public(find(pid))


@app.post("/products/{pid}/reserve", tags=["Stock"])
async def reserve(pid: int, body: Quantity):
    """Réserve du stock pour une commande (appelé par order-service)."""
    p = find(pid)
    if p["stock"] < body.quantity:
        raise HTTPException(
            status_code=409,
            detail=f"Stock insuffisant pour « {p['name']} » : {p['stock']} disponible(s), {body.quantity} demandé(s)",
        )
    p["stock"] -= body.quantity
    p["sold"] += body.quantity
    return public(p)


@app.post("/products/{pid}/release", tags=["Stock"])
async def release(pid: int, body: Quantity):
    """Remet du stock (annulation de commande ou compensation d'une commande échouée)."""
    p = find(pid)
    p["stock"] += body.quantity
    p["sold"] = max(0, p["sold"] - body.quantity)
    return public(p)


@app.put("/products/{pid}/stock", tags=["Stock"])
async def set_stock(pid: int, body: StockUpdate):
    """Réapprovisionnement depuis l'écran Inventaire."""
    p = find(pid)
    p["stock"] = body.stock
    return public(p)
