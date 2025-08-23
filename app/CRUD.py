from sqlalchemy.orm import Session
from app import models, schemas
from datetime import datetime
from fastapi import HTTPException

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session):
    return db.query(models.Product).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_product_by_sku(db: Session, sku: str):
    return db.query(models.Product).filter(models.Product.sku == sku).first()

def update_product(db: Session, db_product: models.Product, updates: schemas.ProductBase):
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(db_product, field, value)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, db_product: models.Product):
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted"}

def create_order(db: Session, order: schemas.OrderCreate):
    product = db.query(models.Product).filter(models.Product.id == order.product_id).first()
    if not product:
        raise ValueError("Product does not exist")
    
    if product.stock < order.quantity:
        raise ValueError("Insufficient stock")
    product.stock -= order.quantity
    db.add(product)

    db_order = models.Order(product_id=order.product_id, quantity = order.quantity, status=order.status)
    db.add(db_order)

    try:
        db.commit()
        db.refresh(db_order)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,detail=f"Order creation failed: {str(e)}")

    return db_order

def get_order(db: Session, skip: int=0):
    return db.query(models.Order).order_by(models.Order.id).offset(skip).all()

def get_order_by_id(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def update_order(
        db: Session,
        db_order: models.Order, 
        updates: schemas.OrderBase
):
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    update_data = updates.dict(exclude_unset=True)

    if "quantity" in updates.dict(exclude_unset=True):
        new_qty = update_data["quantity"]
        diff = updates.quantity - db_order.quantity
        if diff!=0:
            product = db.query(models.Product).with_for_update().filter(models.Product.id == db_order.product_id).first()
            if not product:
                raise HTTPException(status_code=404, detail="Related product not found")
        
            if diff>0:
                if product.stock < diff:
                    raise HTTPException(status_code=409, detail="Insufficient stock to increase quantity")
                product.stock -= diff
            else:
                product.stock += (-diff)
            db.add(product)
        
        db_order.quantity = new_qty

    if "status" in update_data:
        new_status = update_data["status"]
        invalid = (
            (db_order.status == "CANCELLED" and new_status in {"PAID", "SHIPPED"})
            or (db_order.status == "SHIPPED" and new_status in {"PENDING", "PAID"})
        )

        if invalid:
            raise HTTPException(status_code=409, detail=f"Invalid state transition {db_order.status} -> {new_status}")
        db_order.status = new_status
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(
        db: Session,
        db_order: models.Order
):
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    product = db.query(models.Product).with_for_update().filter(models.Product.id == db_order.product_id).first()

    if product:
        product.stock += db_order.id
        db.add(product)
    
    db.delete(db_order)
    db.commit()
    return {"message": "Order deleted successfully"}