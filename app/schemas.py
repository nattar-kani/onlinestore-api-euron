from pydantic import BaseModel, PositiveInt, condecimal
from typing import Literal
from datetime import datetime

class ProductBase(BaseModel):
    sku: str
    name: str
    price: condecimal(gt=0, max_digits=10, decimal_places=2)
    stock: PositiveInt

class ProductCreate(ProductBase):
    class Config:
        schema_extra = {
            "example": {
                "sku": "ANM011",
                "name": "Kakashi Figurine",
                "price": 450.00,
                "stock": 10
            }
        }
    

class ProductOut(ProductBase):
    id: int
    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    product_id: int
    quantity: PositiveInt
    status: Literal["PENDING", "PAID", "SHIPPED", "CANCELLED"] = "PENDING"

class OrderCreate(OrderBase):
    class Config:
        schema_extra = {
            "example": {
                "product_id": 1,
                "quantity": 2,
                "status": "PENDING"
            }
        } 

class OrderOut(OrderBase):
    id: int 
    createdOn: datetime
    class Config:
        orm_mode = True