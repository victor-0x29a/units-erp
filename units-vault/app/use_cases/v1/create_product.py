from documents import Product, Batch
from exceptions import GreaterThanPrice, HasWithSameBatch


class CreateProduct:
    def __init__(self, product_document: Product, product_data: dict, batch_document: Batch = None):
        self.product_document = product_document
        self.batch_document = batch_document
        self.data = product_data
        self._fill_data()
        self._validate()

    def _fill_data(self):
        if "class 'str'" in str(type(self.data.get('batch'))):
            batch = self.batch_document.objects.get(id=self.data.get('batch'))
            self.data['batch'] = batch.id

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

        return [product, self.data]
