from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Query, status

from app.catalog.repository import CatalogRepository
from app.catalog.schemas import (
    CatalogItemCreate,
    CatalogItemResponse,
    CatalogItemStatusUpdate,
    CatalogItemType,
    CatalogItemUpdate,
)
from app.catalog.service import CatalogService

router = APIRouter(prefix="/catalog/items", tags=["catalog"])

catalog_repository = CatalogRepository()
catalog_service = CatalogService(catalog_repository)


@router.post("", response_model=CatalogItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(payload: CatalogItemCreate) -> CatalogItemResponse:
    return catalog_service.create_item(payload)


@router.get("", response_model=List[CatalogItemResponse], status_code=status.HTTP_200_OK)
def list_items(
    item_type: Optional[CatalogItemType] = Query(default=None),
    is_active: Optional[bool] = Query(default=None),
) -> List[CatalogItemResponse]:
    return catalog_service.list_items(item_type=item_type, is_active=is_active)


@router.get("/{item_id}", response_model=CatalogItemResponse, status_code=status.HTTP_200_OK)
def get_item_by_id(item_id: UUID) -> CatalogItemResponse:
    return catalog_service.get_item_by_id(item_id)


@router.patch("/{item_id}", response_model=CatalogItemResponse, status_code=status.HTTP_200_OK)
def update_item(item_id: UUID, payload: CatalogItemUpdate) -> CatalogItemResponse:
    return catalog_service.update_item(item_id, payload)


@router.patch("/{item_id}/status", response_model=CatalogItemResponse, status_code=status.HTTP_200_OK)
def update_item_status(
    item_id: UUID,
    payload: CatalogItemStatusUpdate,
) -> CatalogItemResponse:
    return catalog_service.update_item_status(item_id, payload)