from documents import Product
from exceptions import GreaterThanPrice, HasWithSameBatch


class CreateProduct:
    def __init__(self, product_document: Product, product_data: dict):
        self.product_document = product_document
        self.data = product_data
        self._validate()

    def _validate(self):
        batch = self.data.get('batch')
        product = self.product_document.objects(batch=batch)

        if product:
            raise HasWithSameBatch()

        product_price = self.data.get('price')
        product_discount = self.data.get('discount_value')

        if (product_price, product_discount) and (product_discount > product_price):
            raise GreaterThanPrice()

    def start(self):
        product = self.product_document(**self.data)
        product.save()

        return product
