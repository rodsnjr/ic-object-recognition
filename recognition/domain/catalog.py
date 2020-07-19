from dataclasses import dataclass
from recognition.event import CatalogEvent
from recognition.event import ResponseEvent


@dataclass
class ProcessedCatalog:
    catalog_response: ResponseEvent
    catalog_event: CatalogEvent

    def forward_catalog(self):
        return self.catalog_event is not None
