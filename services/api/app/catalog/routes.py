from typing import List
from uuid import UUID

from fastapi import APIRouter, status

from app.catalog.repository import CatalogRepository
from app.catalog.schemas import CatalogItemCreate, CatalogItemResponse
from app.catalog.service import CatalogService

router = APIRouter(prefix="/catalog/items", tags=["catalog"])

catalog_repository = CatalogRepository()
catalog_service = CatalogService(catalog_repository)


@router.post("", response_model=CatalogItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(payload: CatalogItemCreate) -> CatalogItemResponse:
    return catalog_service.create_item(payload)


@router.get("", response_model=List[CatalogItemResponse], status_code=status.HTTP_200_OK)
def list_items() -> List[CatalogItemResponse]:
    return catalog_service.list_items()


@router.get("/{item_id}", response_model=CatalogItemResponse, status_code=status.HTTP_200_OK)
def get_item_by_id(item_id: UUID) -> CatalogItemResponse:
    return catalog_service.get_item_by_id(item_id)