from typing import List
from uuid import UUID, uuid4

from fastapi import HTTPException, status

from app.catalog.repository import CatalogRepository
from app.catalog.schemas import CatalogItemCreate, CatalogItemResponse


class CatalogService:
    def __init__(self, repository: CatalogRepository) -> None:
        self.repository = repository

    def create_item(self, payload: CatalogItemCreate) -> CatalogItemResponse:
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

    def list_items(self) -> List[CatalogItemResponse]:
        return self.repository.list_all()

    def get_item_by_id(self, item_id: UUID) -> CatalogItemResponse:
        item = self.repository.get_by_id(item_id)

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Catalog item not found",
            )

        return item