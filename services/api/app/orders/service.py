from typing import List
from uuid import UUID, uuid4

from fastapi import HTTPException, status

from app.orders.repository import OrderRepository
from app.orders.schemas import (
    OrderCreate,
    OrderItemResponse,
    OrderResponse,
    OrderStatus,
)


class OrderService:
    def __init__(self, repository: OrderRepository) -> None:
        self.repository = repository

    def create_order(self, payload: OrderCreate) -> OrderResponse:
        items_response: List[OrderItemResponse] = []
        total_amount = 0.0

        for item in payload.items:
            subtotal = item.quantity * item.unit_price
            total_amount += subtotal

            items_response.append(
                OrderItemResponse(
                    product_id=item.product_id,
                    product_name=item.product_name,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    subtotal=subtotal,
                )
            )

        order = OrderResponse(
            id=uuid4(),
            customer_name=payload.customer_name,
            customer_email=payload.customer_email,
            items=items_response,
            total_amount=round(total_amount, 2),
            status=OrderStatus.CREATED,
            shipping_address=payload.shipping_address,
        )

        return self.repository.save(order)

    def get_order_by_id(self, order_id: UUID) -> OrderResponse:
        order = self.repository.get_by_id(order_id)

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )

        return order

    def list_orders(self) -> List[OrderResponse]:
        return self.repository.list_all()