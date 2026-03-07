from typing import Dict, List, Optional
from uuid import UUID

from app.orders.schemas import OrderResponse


class OrderRepository:
    def __init__(self) -> None:
        self._orders: Dict[UUID, OrderResponse] = {}

    def save(self, order: OrderResponse) -> OrderResponse:
        self._orders[order.id] = order
        return order

    def get_by_id(self, order_id: UUID) -> Optional[OrderResponse]:
        return self._orders.get(order_id)

    def list_all(self) -> List[OrderResponse]:
        return list(self._orders.values())