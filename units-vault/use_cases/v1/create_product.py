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
        batch_id_stringified = self.data.get('batch', None)

        batch_field_is_string = "class 'str'" in str(type(batch_id_stringified))

        if batch_field_is_string:
            batch = self.batch_document.objects.get(reference=batch_id_stringified)
            self.data['batch'] = batch.id

    def _validate(self):
        batch = self.data.get('batch')
        product = self.product_document.objects(batch=batch)

        if product:
            """
            If have with same batch, doesn't allow to create, use the route to add more quantity instead.
            """
            raise HasWithSameBatch()

        product_price = self.data.get('price')
        product_discount = self.data.get('discount_value')

        if (product_price, product_discount) and (product_discount > product_price):
            raise GreaterThanPrice()

    def start(self):
        product = self.product_document(**self.data)
        product.save()

        return [product, self.data]
