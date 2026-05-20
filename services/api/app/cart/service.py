from typing import List
from uuid import NAMESPACE_URL, UUID, uuid4, uuid5

from fastapi import HTTPException, status

from app.cart.repository import CartRepository
from app.cart.schemas import (
    BookingDepositDraftCreate,
    BookingDepositDraftItemResponse,
    BookingDepositDraftResponse,
    CartItemCreate,
    CartItemResponse,
    CartItemUpdate,
    CartResponse,
)
from app.catalog.routes import catalog_service
from app.catalog.schemas import CatalogItemType


BOOKING_DEPOSIT_PERCENTAGE = 20
BOOKING_REMAINING_PERCENTAGE = 80


class CartService:
    def __init__(self, repository: CartRepository) -> None:
        self.repository = repository

    def create_cart(self) -> CartResponse:
        cart = CartResponse(
            id=uuid4(),
            items=[],
            subtotal=0.0,
        )

        return self.repository.save(cart)

    def create_booking_deposit_draft(
        self,
        payload: BookingDepositDraftCreate,
    ) -> BookingDepositDraftResponse:
        service_price = (
            round(payload.service_price, 2)
            if payload.service_price is not None
            else None
        )
        deposit_amount = self._calculate_percentage_amount(
            service_price,
            BOOKING_DEPOSIT_PERCENTAGE,
        )
        remaining_amount = self._calculate_percentage_amount(
            service_price,
            BOOKING_REMAINING_PERCENTAGE,
        )
        amount_status = (
            "estimated"
            if service_price is not None
            else "pending_final_price"
        )
        schedule_status = (
            "pending_confirmation"
            if payload.requested_day and payload.requested_time
            else "pending_selection"
        )
        draft_item = BookingDepositDraftItemResponse(
            service_label=payload.service_label,
            professional_label=payload.professional_label,
            professional_id=payload.professional_id,
            professional_role=payload.professional_role,
            quantity=1,
            service_price=service_price,
            deposit_amount=deposit_amount,
            remaining_amount=remaining_amount,
            amount_status=amount_status,
        )

        return BookingDepositDraftResponse(
            draft_id=self._build_booking_deposit_draft_id(payload),
            source=payload.source,
            deposit_percentage=BOOKING_DEPOSIT_PERCENTAGE,
            remaining_percentage=BOOKING_REMAINING_PERCENTAGE,
            total_amount=service_price,
            deposit_amount=deposit_amount,
            remaining_amount=remaining_amount,
            amount_status=amount_status,
            schedule_status=schedule_status,
            requested_day=payload.requested_day,
            requested_time=payload.requested_time,
            cart_count=1,
            items=[draft_item],
        )

    def get_cart_by_id(self, cart_id: UUID) -> CartResponse:
        cart = self.repository.get_by_id(cart_id)

        if not cart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart not found",
            )

        return cart

    def add_item(
        self,
        cart_id: UUID,
        payload: CartItemCreate,
    ) -> CartResponse:
        cart = self.get_cart_by_id(cart_id)
        catalog_item = catalog_service.get_item_by_id(payload.catalog_item_id)

        if not catalog_item.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Catalog item is not active",
            )

        self._validate_quantity_rules(catalog_item.item_type, payload.quantity)
        self._validate_stock(catalog_item.stock, payload.quantity)

        existing_item = next(
            (
                item
                for item in cart.items
                if item.catalog_item_id == payload.catalog_item_id
            ),
            None,
        )

        updated_items: List[CartItemResponse]

        if existing_item:
            if catalog_item.item_type == CatalogItemType.SERVICE:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Service items can only be added once per cart",
                )

            new_quantity = existing_item.quantity + payload.quantity
            self._validate_stock(catalog_item.stock, new_quantity)

            updated_items = []

            for item in cart.items:
                if item.catalog_item_id == payload.catalog_item_id:
                    updated_items.append(
                        CartItemResponse(
                            catalog_item_id=item.catalog_item_id,
                            name=item.name,
                            item_type=item.item_type,
                            unit_price=item.unit_price,
                            quantity=new_quantity,
                            subtotal=round(item.unit_price * new_quantity, 2),
                        )
                    )
                else:
                    updated_items.append(item)

        else:
            new_item = CartItemResponse(
                catalog_item_id=catalog_item.id,
                name=catalog_item.name,
                item_type=catalog_item.item_type,
                unit_price=round(catalog_item.price, 2),
                quantity=payload.quantity,
                subtotal=round(catalog_item.price * payload.quantity, 2),
            )

            updated_items = cart.items + [new_item]

        updated_cart = self._build_updated_cart(cart, updated_items)
        return self.repository.update(updated_cart)

    def update_item_quantity(
        self,
        cart_id: UUID,
        catalog_item_id: UUID,
        payload: CartItemUpdate,
    ) -> CartResponse:
        cart = self.get_cart_by_id(cart_id)
        catalog_item = catalog_service.get_item_by_id(catalog_item_id)

        if not catalog_item.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Catalog item is not active",
            )

        self._validate_quantity_rules(catalog_item.item_type, payload.quantity)
        self._validate_stock(catalog_item.stock, payload.quantity)

        found = False
        updated_items: List[CartItemResponse] = []

        for item in cart.items:
            if item.catalog_item_id == catalog_item_id:
                found = True
                updated_items.append(
                    CartItemResponse(
                        catalog_item_id=item.catalog_item_id,
                        name=item.name,
                        item_type=item.item_type,
                        unit_price=item.unit_price,
                        quantity=payload.quantity,
                        subtotal=round(item.unit_price * payload.quantity, 2),
                    )
                )
            else:
                updated_items.append(item)

        if not found:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found",
            )

        updated_cart = self._build_updated_cart(cart, updated_items)
        return self.repository.update(updated_cart)

    def remove_item(
        self,
        cart_id: UUID,
        catalog_item_id: UUID,
    ) -> CartResponse:
        cart = self.get_cart_by_id(cart_id)

        if not any(item.catalog_item_id == catalog_item_id for item in cart.items):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found",
            )

        updated_items = [
            item for item in cart.items
            if item.catalog_item_id != catalog_item_id
        ]

        updated_cart = self._build_updated_cart(cart, updated_items)
        return self.repository.update(updated_cart)

    def _build_updated_cart(
        self,
        cart: CartResponse,
        items: List[CartItemResponse],
    ) -> CartResponse:
        subtotal = round(sum(item.subtotal for item in items), 2)

        return cart.model_copy(
            update={
                "items": items,
                "subtotal": subtotal,
            }
        )

    def _validate_quantity_rules(
        self,
        item_type: CatalogItemType,
        quantity: int,
    ) -> None:
        if item_type == CatalogItemType.SERVICE and quantity != 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Service items must have quantity equal to 1",
            )

    def _validate_stock(
        self,
        stock: int | None,
        quantity: int,
    ) -> None:
        if stock is not None and quantity > stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Requested quantity exceeds available stock",
            )

    def _calculate_percentage_amount(
        self,
        amount: float | None,
        percentage: int,
    ) -> float | None:
        if amount is None:
            return None

        return round(amount * percentage / 100, 2)

    def _build_booking_deposit_draft_id(
        self,
        payload: BookingDepositDraftCreate,
    ) -> UUID:
        seed = "|".join(
            [
                payload.source,
                payload.service_label,
                payload.professional_label,
                payload.professional_id or "",
                payload.professional_role or "",
                payload.requested_day or "",
                payload.requested_time or "",
                str(payload.service_price or ""),
            ]
        )

        return uuid5(NAMESPACE_URL, f"always-beautiful:cart:{seed}")
