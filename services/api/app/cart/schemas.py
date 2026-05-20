from typing import List, Literal
from uuid import UUID

from pydantic import BaseModel, Field, model_validator

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


class BookingDepositDraftItemCreate(BaseModel):
    service_label: str = Field(..., min_length=2, max_length=120)
    professional_label: str = Field(..., min_length=2, max_length=120)
    professional_id: str | None = Field(default=None, max_length=80)
    professional_role: str | None = Field(default=None, max_length=120)
    service_price: float | None = Field(default=None, gt=0)


class BookingDepositDraftCreate(BaseModel):
    assistant_session_id: str = Field(..., min_length=2, max_length=120)
    items: List[BookingDepositDraftItemCreate] | None = None
    service_label: str | None = Field(default=None, min_length=2, max_length=120)
    professional_label: str | None = Field(default=None, min_length=2, max_length=120)
    professional_id: str | None = Field(default=None, max_length=80)
    professional_role: str | None = Field(default=None, max_length=120)
    requested_day: str | None = Field(default=None, max_length=40)
    requested_time: str | None = Field(default=None, max_length=20)
    service_price: float | None = Field(default=None, gt=0)
    source: Literal["assistant", "web", "admin"] = "assistant"

    @model_validator(mode="after")
    def validate_items_or_legacy_fields(self):
        if self.items is not None:
            if not self.items:
                raise ValueError("items must include at least one service")

            return self

        if not self.service_label or not self.professional_label:
            raise ValueError(
                "service_label and professional_label are required when "
                "items is not provided"
            )

        return self


class BookingDepositDraftItemResponse(BaseModel):
    service_label: str
    professional_label: str
    professional_id: str | None = None
    professional_role: str | None = None
    quantity: int
    service_price: float | None = None
    deposit_amount: float | None = None
    remaining_amount: float | None = None
    amount_status: Literal["estimated", "pending_final_price"]


class BookingDepositDraftResponse(BaseModel):
    draft_id: UUID
    type: Literal["booking_deposit_draft"] = "booking_deposit_draft"
    status: Literal["draft"] = "draft"
    source: Literal["assistant", "web", "admin"]
    assistant_session_id: str
    deposit_percentage: int
    remaining_percentage: int
    total_amount: float | None = None
    deposit_amount: float | None = None
    remaining_amount: float | None = None
    amount_status: Literal["estimated", "pending_final_price"]
    schedule_status: Literal["pending_selection", "pending_confirmation"]
    confirmation_status: Literal["not_confirmed"] = "not_confirmed"
    payment_status: Literal["not_executed"] = "not_executed"
    booking_status: Literal["not_created"] = "not_created"
    order_status: Literal["not_created"] = "not_created"
    requested_day: str | None = None
    requested_time: str | None = None
    cart_count: int
    items: List[BookingDepositDraftItemResponse] = Field(default_factory=list)
