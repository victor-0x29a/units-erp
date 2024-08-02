from use_cases import CreateProductV1


class ProductService:
    def create(self, data={}):
        CreateProductV1(
            product_data=data
        ).start()
