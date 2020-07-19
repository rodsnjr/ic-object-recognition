from faust import Record
from enum import Enum


class ResponseStatus(Enum):
    NOT_FOUND = 'NotFound'
    FOUND = 'Found'


class ResponseEvent(Record, serializer='json'):
    uid: str
    catalog_event_id: str
    catalog_id: str
    subject: str
    image_key: str
    subject: str
    filters: str
    status: str
