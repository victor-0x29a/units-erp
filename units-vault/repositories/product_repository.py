from documents import Product
from exceptions import MissingParam, MissingDoc


class ProductRepository:
    def __init__(self, product_document: Product):
        self.Product = product_document

    def delete(self, product: Product) -> None:
        if not product:
            raise MissingParam('Product is required.')

        product.delete()

    def get(self, filters=None, can_raises=True) -> Product:
        if not filters:
            raise MissingParam("Filter is required.")

        product = self.Product.objects(**filters).first()

        if not product and can_raises:
            raise MissingDoc("Product not found.")

        return product
