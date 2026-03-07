from typing import Dict, List
from uuid import UUID, uuid4

from fastapi import HTTPException, status

from app.orders.repository import OrderRepository
from app.orders.schemas import (
    OrderCreate,
    OrderItemResponse,
    OrderPaymentLink,
    OrderResponse,
    OrderShippingLink,
    OrderStatus,
)


class OrderService:
    def __init__(self, repository: OrderRepository) -> None:
        self.repository = repository
        self.allowed_transitions: Dict[OrderStatus, set[OrderStatus]] = {
            OrderStatus.CREATED: {
                OrderStatus.PAYMENT_PENDING,
                OrderStatus.CANCELLED,
            },
            OrderStatus.PAYMENT_PENDING: {
                OrderStatus.PAID,
                OrderStatus.CANCELLED,
            },
            OrderStatus.PAID: {
                OrderStatus.FULFILLING,
            },
            OrderStatus.FULFILLING: {
                OrderStatus.SHIPPED,
            },
            OrderStatus.SHIPPED: {
                OrderStatus.COMPLETED,
            },
            OrderStatus.COMPLETED: set(),
            OrderStatus.CANCELLED: set(),
        }

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
            payment_id=None,
            shipping_id=None,
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

    def update_order_status(self, order_id: UUID, new_status: OrderStatus) -> OrderResponse:
        order = self.get_order_by_id(order_id)

        allowed = self.allowed_transitions.get(order.status, set())
        if new_status not in allowed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status transition from {order.status} to {new_status}",
            )

        updated_order = order.model_copy(update={"status": new_status})
        return self.repository.update(updated_order)

    def link_payment(self, order_id: UUID, payload: OrderPaymentLink) -> OrderResponse:
        order = self.get_order_by_id(order_id)
        updated_order = order.model_copy(update={"payment_id": payload.payment_id})
        return self.repository.update(updated_order)

    def link_shipping(self, order_id: UUID, payload: OrderShippingLink) -> OrderResponse:
        order = self.get_order_by_id(order_id)
        updated_order = order.model_copy(update={"shipping_id": payload.shipping_id})
        return self.repository.update(updated_order)