from documents import Product, Batch
from exceptions import GreaterThanPrice, HasWithSameBatch


class CreateProduct:
    def __init__(self, product_data: dict):
        self.data = product_data

        self.product_obj = Product(**self.data)

        self.product_obj.validate()

        self.__fill_data()
        self.__validate()

    def __fill_data(self):
        batch_id_stringified = self.data.get('batch', None)

        batch_field_is_string = "class 'str'" in str(type(batch_id_stringified))

        if batch_field_is_string:
            """
            IF BATCH IS STRING, FIND THE BATCH BY REFERENCE
            """
            batch = Batch.objects.get(reference=batch_id_stringified)
            self.data['batch'] = batch.id

    def __validate(self):
        batch = self.data.get('batch')
        product = Product.objects(batch=batch)

        if product:
            """
            If have with same batch, doesn't allow to create, use the route to add more quantity instead.
            """
            raise HasWithSameBatch()

        product_price = self.data.get('price')
        product_discount = self.data.get('discount_value')

        if (product_price and product_discount) and (product_discount > product_price):
            raise GreaterThanPrice()

    def start(self):
        self.product_obj.save()

        return self.product_obj
