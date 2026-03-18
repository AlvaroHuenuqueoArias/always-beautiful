from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


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

    @field_validator("item_type", mode="before")
    @classmethod
    def normalize_item_type(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value


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