from mongoengine import Document, StringField, DateTimeField, DateField, ValidationError
from pycpfcnpj import cpfcnpj


def _is_valid_cnpj(value):
    is_valid_cnpj = cpfcnpj.validate(value)

    if value and not is_valid_cnpj:
        raise ValidationError('The company doc should be valid.')


class Batch(Document):
    supplier_document = StringField(required=True, validation=_is_valid_cnpj)
    reference = StringField(required=True, unique=True)
    inserction_datetime = DateTimeField(required=True)
    expiry_date = DateField(required=True)
