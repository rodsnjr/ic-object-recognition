from recognition import util
from recognition.event import CatalogEvent, CatalogChildEvent
from recognition.event import ResponseEvent, ResponseStatus
from recognition.domain import ProcessedCatalog
from recognition.domain import ObjectRecognition
from recognition.providers import cache_client, file_client
from PIL import Image
from io import BytesIO
from . import recognition as recognition


def _build_response_event(object_recognition: ObjectRecognition,
                          catalog_event: CatalogEvent) -> ResponseEvent:
    status = ResponseStatus.FOUND if object_recognition.has_predictions(catalog_event.filters) \
                                  else ResponseStatus.NOT_FOUND
    return ResponseEvent(
        uid=util.generate_uid(),
        catalog_event_id=catalog_event.uid,
        catalog_id=catalog_event.catalog_id,
        subject=catalog_event.subject,
        image_key=catalog_event.image_key,
        filters=catalog_event.filters,
        status=status
    )


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
    return cache_client.get(catalog_event.uid) is not None


def add_processed(catalog_event: CatalogEvent):
    pass


async def _load_image(key):
    img_bytes = await file_client.download_bytes(key)
    image = Image.open(BytesIO(img_bytes))
    return image


async def process_catalog_event(catalog_event: CatalogEvent) -> ProcessedCatalog:
    # Object Recognition
    img = await _load_image(catalog_event.image_key)
    object_recognition = recognition.recognize(image=img,
                                               catalod_id=catalog_event.catalog_id,
                                               event_id=catalog_event.uid)
    await recognition.save(object_recognition)

    # Forward Events
    response_event = _build_response_event(object_recognition,
                                           catalog_event)
    forward_event = _build_forward_catalog(catalog_event)

    return ProcessedCatalog(catalog_response=response_event,
                            catalog_event=forward_event)
