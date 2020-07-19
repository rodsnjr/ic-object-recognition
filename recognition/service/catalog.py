from typing import List

from recognition.event import CatalogEvent, CatalogChildEvent, ResponseEvent
from recognition.domain import ProcessedCatalog
from recognition.domain import ObjectRecognition
from . import image
from . import recognition as recognition


def _build_response_event(object_recognition: ObjectRecognition,
                          filters: List[str]) -> ResponseEvent:
    pass


def _build_forward_catalog(catalog_event: CatalogEvent) -> CatalogEvent | None:
    if catalog_event.children is not None:
        first_child: CatalogChildEvent = catalog_event.children.pop()
        return CatalogEvent(
            uid=first_child.uid,
            image_key=catalog_event.image_key,
            catalog_id=catalog_event.catalog_id,
            filters=first_child.filters,
            subject=first_child.subject,
            children=catalog_event.children,
        )
    return None


def has_processed(catalog_event: CatalogEvent) -> bool:
    return True


async def process_catalog_event(catalog_event: CatalogEvent) -> ProcessedCatalog:
    # Object Recognition
    img = image.resize_image(await image.load_image(catalog_event.image_key))
    object_recognition = recognition.recognize(img)
    object_recognition.catalog_id = catalog_event.catalog_id
    object_recognition.event_id = catalog_event.uid
    await recognition.save(object_recognition)

    # Forward Events
    response_event = _build_response_event(object_recognition,
                                           catalog_event.filters)
    forward_event = _build_forward_catalog(catalog_event)

    return ProcessedCatalog(catalog_response=response_event,
                            catalog_event=forward_event)
