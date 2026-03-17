from typing import List
from uuid import UUID, uuid4

from fastapi import HTTPException, status

from app.cart.repository import CartRepository
from app.cart.schemas import (
    CartItemCreate,
    CartItemResponse,
    CartItemUpdate,
    CartResponse,
)
from app.catalog.routes import catalog_service
from app.catalog.schemas import CatalogItemType


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