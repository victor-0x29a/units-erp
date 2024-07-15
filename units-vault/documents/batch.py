from mongoengine import Document, StringField, DateTimeField, DateField


class Batch(Document):
    supplier_document = StringField(required=True)
    reference = StringField(required=True, unique=True)
    inserction_datetime = DateTimeField(required=True)
    expiry_date = DateField(required=True)
