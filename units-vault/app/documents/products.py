from mongoengine import Document, StringField, FloatField, IntField, ReferenceField
from batch import Batch
from constants import PRODUCT_DATA_TYPES
import time
import barcode
from barcode.writer import ImageWriter


class Product(Document):
    name = StringField(required=True)
    barcode = StringField(required=True, unique=True, min_length=13, max_length=13, regex='^[0-9]*$')
    price = FloatField(required=True)
    stock = IntField(required=True)
    batch = ReferenceField(Batch, required=True)
    discount_value = FloatField(default=0.0)
    item_type = StringField(required=True)
    data_type = StringField(required=True,
                            default=PRODUCT_DATA_TYPES['for_sale'],
                            choices=PRODUCT_DATA_TYPES.values())

    def save(self, *args, **kwargs):
        if not self.barcode:
            self.barcode = self.generate_unique_barcode()

        super(Product, self).save(*args, **kwargs)

    @staticmethod
    def generate_unique_barcode():
        while True:
            timestamp = str(time.time())[:12]

            if len(timestamp) < 12:
                timestamp = timestamp.ljust(12, '0')

            ean = barcode.get('ean13', timestamp, writer=ImageWriter())

            barcode_number = str(ean.get_fullcode())

            if not Product.objects(barcode=barcode_number):
                return barcode_number
