from typing import List, Optional
from uuid import UUID, uuid4

from fastapi import HTTPException, status

from app.catalog.repository import CatalogRepository
from app.catalog.schemas import (
    CatalogItemCreate,
    CatalogItemResponse,
    CatalogItemStatusUpdate,
    CatalogItemType,
    CatalogItemUpdate,
)


class CatalogService:
    def __init__(self, repository: CatalogRepository) -> None:
        self.repository = repository

    def create_item(self, payload: CatalogItemCreate) -> CatalogItemResponse:
        self._validate_catalog_rules(payload.item_type, payload.stock)

        item = CatalogItemResponse(
            id=uuid4(),
            name=payload.name,
            description=payload.description,
            item_type=payload.item_type,
            price=round(payload.price, 2),
            stock=payload.stock,
            is_active=payload.is_active,
        )

        return self.repository.save(item)

    def list_items(
        self,
        item_type: Optional[CatalogItemType] = None,
        is_active: Optional[bool] = None,
    ) -> List[CatalogItemResponse]:
        items = self.repository.list_all()

        if item_type is not None:
            items = [item for item in items if item.item_type == item_type]

        if is_active is not None:
            items = [item for item in items if item.is_active == is_active]

        return items

    def get_item_by_id(self, item_id: UUID) -> CatalogItemResponse:
        item = self.repository.get_by_id(item_id)

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Catalog item not found",
            )

        return item

    def update_item(
        self,
        item_id: UUID,
        payload: CatalogItemUpdate,
    ) -> CatalogItemResponse:
        item = self.get_item_by_id(item_id)

        updated_item = item.model_copy(
            update=payload.model_dump(exclude_unset=True)
        )

        self._validate_catalog_rules(updated_item.item_type, updated_item.stock)

        updated_item = updated_item.model_copy(
            update={"price": round(updated_item.price, 2)}
        )

        return self.repository.update(updated_item)

    def update_item_status(
        self,
        item_id: UUID,
        payload: CatalogItemStatusUpdate,
    ) -> CatalogItemResponse:
        item = self.get_item_by_id(item_id)

        updated_item = item.model_copy(
            update={"is_active": payload.is_active}
        )

        return self.repository.update(updated_item)

    def _validate_catalog_rules(
        self,
        item_type: CatalogItemType,
        stock: Optional[int],
    ) -> None:
        if item_type == CatalogItemType.SERVICE and stock is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Service items must not define stock",
            )