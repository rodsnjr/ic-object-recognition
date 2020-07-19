from faust import Record


class ResponseEvent(Record, serializer='json'):
    pass
