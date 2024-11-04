from mongoengine import Document, StringField, FloatField, IntField


class Store(Document):
    name = StringField(required=True, max_length=60)
    latitude = FloatField(required=False, default=0)
    longitude = FloatField(required=False, default=0)
    unit = IntField(required=True, unique=True)
