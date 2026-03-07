from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr


class OrderStatus(str, Enum):
    CREATED = "CREATED"
    PAYMENT_PENDING = "PAYMENT_PENDING"
    PAID = "PAID"
    FULFILLING = "FULFILLING"
    SHIPPED = "SHIPPED"
    COMPLETED = "COMPLETED"


class OrderItemCreate(BaseModel):
    product_id: str = Field(..., min_length=1, max_length=100)
    product_name: str = Field(..., min_length=1, max_length=255)
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)


class OrderCreate(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=120)
    customer_email: EmailStr
    items: List[OrderItemCreate] = Field(..., min_length=1)
    shipping_address: Optional[str] = Field(default=None, max_length=255)


class OrderItemResponse(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    unit_price: float
    subtotal: float


class OrderResponse(BaseModel):
    id: UUID
    customer_name: str
    customer_email: EmailStr
    items: List[OrderItemResponse]
    total_amount: float
    status: OrderStatus
    shipping_address: Optional[str] = None