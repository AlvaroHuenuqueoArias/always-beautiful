from uuid import UUID

from fastapi import APIRouter, status

from app.cart.repository import CartRepository
from app.cart.schemas import (
    BookingDepositDraftCreate,
    BookingDepositDraftResponse,
    CartItemCreate,
    CartItemUpdate,
    CartResponse,
)
from app.cart.service import CartService

router = APIRouter(prefix="/cart", tags=["cart"])

cart_repository = CartRepository()
cart_service = CartService(cart_repository)


@router.post("", response_model=CartResponse, status_code=status.HTTP_201_CREATED)
def create_cart() -> CartResponse:
    return cart_service.create_cart()


@router.post(
    "/booking-deposit/draft",
    response_model=BookingDepositDraftResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_booking_deposit_draft(
    payload: BookingDepositDraftCreate,
) -> BookingDepositDraftResponse:
    return cart_service.create_booking_deposit_draft(payload)


@router.get("/{cart_id}", response_model=CartResponse, status_code=status.HTTP_200_OK)
def get_cart_by_id(cart_id: UUID) -> CartResponse:
    return cart_service.get_cart_by_id(cart_id)


@router.post("/{cart_id}/items", response_model=CartResponse, status_code=status.HTTP_200_OK)
def add_item(cart_id: UUID, payload: CartItemCreate) -> CartResponse:
    return cart_service.add_item(cart_id, payload)


@router.patch("/{cart_id}/items/{catalog_item_id}", response_model=CartResponse, status_code=status.HTTP_200_OK)
def update_item_quantity(
    cart_id: UUID,
    catalog_item_id: UUID,
    payload: CartItemUpdate,
) -> CartResponse:
    return cart_service.update_item_quantity(cart_id, catalog_item_id, payload)


@router.delete("/{cart_id}/items/{catalog_item_id}", response_model=CartResponse, status_code=status.HTTP_200_OK)
def remove_item(
    cart_id: UUID,
    catalog_item_id: UUID,
) -> CartResponse:
    return cart_service.remove_item(cart_id, catalog_item_id)
