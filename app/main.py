from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, CRUD
from app.database import engine, Base, get_db
from app.auth import get_apikey
from app.routers.webhook import webhook_router


Base.metadata.create_all(bind=engine)
app = FastAPI(title="Online Store API", version="1.0", description="Products & Orders with API key auth", contact={
    "github": "nattar-kani"
})

app.include_router(webhook_router)

@app.post("/products", response_model=schemas.ProductOut)
def create_product(
    createProduct: schemas.ProductCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_apikey)
):
    """Create a new product"""
    existing = CRUD.get_product_by_sku(db, createProduct.sku)
    if existing:
        raise HTTPException(status_code=409, detail="SKU already exists")
    db_product = CRUD.create_product(db,createProduct)
    return db_product

@app.get("/products", response_model=list[schemas.ProductOut])
def list_products(
        db: Session = Depends(get_db),
        api_key: str = Depends(get_apikey)
):
    """List all products"""
    return CRUD.get_products(db)

@app.get("/products/{product_id}", response_model=schemas.ProductOut)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_apikey)
):
    """Place a new order"""
    db_product = CRUD.get_product_by_id(db,product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.put("/products/{product_id}", response_model=schemas.ProductOut)
def update_product(
    product_id: int,
    updates: schemas.ProductBase,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_apikey),
):
    """Update a product"""
    db_product = CRUD.get_product_by_id(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return CRUD.update_product(db, db_product, updates)

@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_apikey)
):
    """Delete a product"""
    db_product = CRUD.get_product_by_id(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return CRUD.delete_product(db, db_product)

@app.post("/orders", response_model=schemas.OrderOut)
def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_apikey)
):
    """Create an order"""
    try:
        db_order = CRUD.create_order(db=db,order=order)
        return db_order
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    
@app.get("/orders/{order_id}", response_model=list[schemas.OrderOut])
def list_order(
    db: Session = Depends(get_db),
    api_key: str = Depends(get_apikey)
):
    """List the orders"""
    return CRUD.get_order(db)

@app.get("/orders/{order_id}", response_model=schemas.OrderOut)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_apikey)
):
    """Get the order details"""
    order = CRUD.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.put("/orders/{order_id}", response_model=schemas.OrderOut)
def update_order(
    order_id: int,
    updates: schemas.OrderBase,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_apikey)
):
    """Update the order"""
    db_order = CRUD.get_order_by_id(db,order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return CRUD.update_order(db, db_order, updates)

@app.delete("/orders/{order_id}")
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_apikey)
):
    """Delete an order"""
    db_order = CRUD.get_order_by_id(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return CRUD.delete_order(db, db_order)