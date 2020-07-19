from recognition.event import CatalogEvent


class BusinessException(Exception):
    pass


def handle_exceptions(catalog_event: CatalogEvent, e: Exception) -> bool:
    pass
