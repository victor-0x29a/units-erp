from documents import Product, Batch
from mongoengine.errors import NotUniqueError
from exceptions import GreaterThanPrice, HasWithSameBatch, MissingDoc, UniqueKey


class CreateProduct:
    def __init__(self, product_data: dict):
        self.data = product_data

        self.product_obj = Product(**product_data)

        self.product_obj.validate()

        self.__fill_data()
        self.__validate()

    def __is_string(self, data):
        return "class 'str'" in str(type(data))

    def __fill_data(self):
        batch = self.data.get('batch', None)

        batch_field_is_string = self.__is_string(batch)

        if batch_field_is_string:
            """
            IF BATCH IS STRING, FIND THE BATCH BY REFERENCE
            """
            try:
                batch = Batch.objects.get(reference=batch)
            except Batch.DoesNotExist:
                raise MissingDoc(message="Batch not found.")

            self.product_obj.batch = batch.id
            self.data['batch'] = batch.id

    def __validate(self):
        batch = self.data.get('batch')

        if not batch:
            raise MissingDoc(message="Missing batch.")

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
        try:
            self.product_obj.save()
        except NotUniqueError:
            raise UniqueKey("Product with same bar code already exists.")

        return self.product_obj
