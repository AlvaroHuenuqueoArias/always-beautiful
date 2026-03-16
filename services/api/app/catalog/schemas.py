from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CatalogItemType(str, Enum):
    PRODUCT = "PRODUCT"
    SERVICE = "SERVICE"


class CatalogItemCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    description: Optional[str] = Field(default=None, max_length=500)
    item_type: CatalogItemType
    price: float = Field(..., gt=0)
    stock: Optional[int] = Field(default=None, ge=0)
    is_active: bool = True


class CatalogItemUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=120)
    description: Optional[str] = Field(default=None, max_length=500)
    price: Optional[float] = Field(default=None, gt=0)
    stock: Optional[int] = Field(default=None, ge=0)


class CatalogItemStatusUpdate(BaseModel):
    is_active: bool


class CatalogItemResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    item_type: CatalogItemType
    price: float
    stock: Optional[int] = None
    is_active: bool