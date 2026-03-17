from typing import Dict, Optional
from uuid import UUID

from app.cart.schemas import CartResponse


class CartRepository:
    def __init__(self) -> None:
        self._carts: Dict[UUID, CartResponse] = {}

    def save(self, cart: CartResponse) -> CartResponse:
        self._carts[cart.id] = cart
        return cart

    def get_by_id(self, cart_id: UUID) -> Optional[CartResponse]:
        return self._carts.get(cart_id)

    def update(self, cart: CartResponse) -> CartResponse:
        self._carts[cart.id] = cart
        return cart