from mongoengine import ObjectIdField
from documents import Product
from exceptions import MissingParam, MissingDoc, HasWithSameBatch, GreaterThanPrice, AlreadyExists


class ProductRepository:
    def __init__(self, product_document: Product):
        self.Product = product_document

    def delete(self, product: Product) -> None:
        if not product:
            raise MissingParam('Product is required.')

        product.delete()

    def get(self, filter=None, can_raises=True) -> Product:
        if not filter:
            raise MissingParam("Filter is required.")

        product = self.Product.objects(**filter).first()

        if not product and can_raises:
            raise MissingDoc("Product not found.")

        return product

    def create(self, data: dict) -> Product:
        self.__check_if_has_already_exists_by_batch_and_bar_code(
            batch_pk=data['batch'],
            bar_code=data['bar_code']
        )

        self.__validate_discount_value(
            discount_value=data.get('discount_value'),
            price=data.get('price')
        )

        product = self.Product(**data)

        product.save()

        return product

    def __validate_discount_value(self, discount_value: float, price: float) -> None:
        if discount_value > price:
            raise GreaterThanPrice()

    def __check_if_has_already_exists_by_batch_and_bar_code(
        self,
        batch_pk: ObjectIdField,
        bar_code: str
    ) -> None:
        product_by_batch = self.Product.objects(batch=batch_pk)

        if product_by_batch:
            raise HasWithSameBatch()

        product_by_bar_code = self.Product.objects(bar_code=bar_code)

        if product_by_bar_code:
            raise AlreadyExists('Product already exists by bar code.')
