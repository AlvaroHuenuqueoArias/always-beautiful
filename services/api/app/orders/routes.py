from typing import List
from uuid import UUID

from fastapi import APIRouter, status

from app.orders.repository import OrderRepository
from app.orders.schemas import OrderCreate, OrderResponse
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