from tortoise.models import Model
from tortoise.fields import JSONField, TextField, DatetimeField


class ObjectRecognitionEntity(Model):
    uid = TextField(pk=True)
    predictions = JSONField()
    catalog_id = TextField()
    event_id = TextField()
    created_time = DatetimeField()
