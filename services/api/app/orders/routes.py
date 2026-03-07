from typing import List
from uuid import UUID

from fastapi import APIRouter, status

from app.orders.repository import OrderRepository
from app.orders.schemas import (
    OrderCreate,
    OrderPaymentLink,
    OrderResponse,
    OrderShippingLink,
    OrderStatusUpdate,
)
from app.orders.service import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])

order_repository = OrderRepository()
order_service = OrderService(order_repository)


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate) -> OrderResponse:
    return order_service.create_order(payload)


@router.get("", response_model=List[OrderResponse], status_code=status.HTTP_200_OK)
def list_orders() -> List[OrderResponse]:
    return order_service.list_orders()


@router.get("/{order_id}", response_model=OrderResponse, status_code=status.HTTP_200_OK)
def get_order_by_id(order_id: UUID) -> OrderResponse:
    return order_service.get_order_by_id(order_id)


@router.patch("/{order_id}/status", response_model=OrderResponse, status_code=status.HTTP_200_OK)
def update_order_status(order_id: UUID, payload: OrderStatusUpdate) -> OrderResponse:
    return order_service.update_order_status(order_id, payload.status)


@router.patch("/{order_id}/payment", response_model=OrderResponse, status_code=status.HTTP_200_OK)
def link_order_payment(order_id: UUID, payload: OrderPaymentLink) -> OrderResponse:
    return order_service.link_payment(order_id, payload)


@router.patch("/{order_id}/shipping", response_model=OrderResponse, status_code=status.HTTP_200_OK)
def link_order_shipping(order_id: UUID, payload: OrderShippingLink) -> OrderResponse:
    return order_service.link_shipping(order_id, payload)