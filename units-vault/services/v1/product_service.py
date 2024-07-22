from documents import Batch, Product
from use_cases import CreateProductV1


class ProductService:
    def create(self, data={}):
        data = data.dict()
        create_payload = {
            **data,
            "item_type": data.get("type"),
            "data_type": data.get("for_use"),
            "stock": data.get("base_stock")
        }

        create_payload.pop("type")
        create_payload.pop("for_use")
        create_payload.pop("base_stock")

        # TO DO: Wait implementation of Batch

        CreateProductV1(
            batch_document=Batch,
            product_document=Product,
            product_data=create_payload
        ).start()
