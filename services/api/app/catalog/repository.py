from typing import Dict, List, Optional
from uuid import UUID

from app.catalog.schemas import CatalogItemResponse


class CatalogRepository:
    def __init__(self) -> None:
        self._items: Dict[UUID, CatalogItemResponse] = {}

    def save(self, item: CatalogItemResponse) -> CatalogItemResponse:
        self._items[item.id] = item
        return item

    def get_by_id(self, item_id: UUID) -> Optional[CatalogItemResponse]:
        return self._items.get(item_id)

    def list_all(self) -> List[CatalogItemResponse]:
        return list(self._items.values())