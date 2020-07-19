from dataclasses import dataclass
from typing import List
from faust import Record


@dataclass
class CatalogChildEvent:
    uid: str
    subject: str
    filters: List[str]


@dataclass
class CatalogEvent(Record, serializer='json'):
    uid: str
    image_key: str
    catalog_id: str
    subject: str
    filters: List[str]
    children: List[CatalogChildEvent]
    retries: int = 0

