from typing import List
from uuid import UUID

from pydantic import BaseModel, Field

from app.catalog.schemas import CatalogItemType


class CartItemCreate(BaseModel):
    catalog_item_id: UUID
    quantity: int = Field(..., gt=0)


class CartItemUpdate(BaseModel):
    quantity: int = Field(..., gt=0)


class CartItemResponse(BaseModel):
    catalog_item_id: UUID
    name: str
    item_type: CatalogItemType
    unit_price: float
    quantity: int
    subtotal: float


class CartResponse(BaseModel):
    id: UUID
    items: List[CartItemResponse] = Field(default_factory=list)
    subtotal: float