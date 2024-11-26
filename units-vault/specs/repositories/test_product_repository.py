import pytest
from datetime import timedelta
from documents import Store, Product, Batch
from use_cases import CreateProductV1
from utils.dates import get_now
from repositories import StoreRepository, ProductRepository, BatchRepository
from exceptions import MissingParam, MissingDoc
from ..fixture import mongo_connection # noqa: F401, E261
from ..__mocks__.constants import company_doc


class TestGet:
    def test_should_get(self, mocker):
        batch_repository = BatchRepository(batch_document=Batch)
        store_repository = StoreRepository(store_document=Store)
        product_repository = ProductRepository(product_document=Product)

        store = store_repository.create(data={
            "unit": 1,
            "name": "Store 1"
        })

        batch = batch_repository.create(data={
            "expiry_date": get_now() + timedelta(days=1),
            "inserction_datetime": get_now(),
            "supplier_document": company_doc,
            "reference": "REFERER001",
            "store": store.pk
        })

        assert batch

        CreateProductV1(product_data={
            'batch': batch.pk,
            'price': 10,
            'discount_value': 1,
            'bar_code': '1234567891012',
            'name': 'foo name',
            'stock': 5,
            'item_type': 'foo type'
        }).start()

        product = product_repository.get(filters={'name': 'foo name'}, can_raises=False)

        assert product
        assert product.price == 10.0

    def test_should_fails_when_unexists(self, mocker):
        product_repository = ProductRepository(product_document=Product)

        with pytest.raises(MissingDoc) as error:
            product_repository.get(filters={
                'name': 'foo'
            })

        assert error.value.message == 'Product not found.'

    def test_should_not_fails_when_unexists_and_cant_raises(self, mocker):
        product_repository = ProductRepository(product_document=Product)

        product = product_repository.get(filters={
            'name': 'foo'
        }, can_raises=False)

        assert not product

    def test_should_fails_when_havent_filters(self, mocker):
        product_repository = ProductRepository(product_document=Product)

        with pytest.raises(MissingParam) as error:
            product_repository.get(filters=None)

        assert error.value.message == 'Filter is required.'


class TestDelete:
    def test_should_delete(self, mocker):
        product_repository = ProductRepository(product_document=Product)
        store_repository = StoreRepository(store_document=Store)
        batch_repository = BatchRepository(batch_document=Batch)

        store_repository.create(data={
            "unit": 1,
            "name": "Store 1"
        })

        batch = batch_repository.create(data={
            "expiry_date": get_now() + timedelta(days=1),
            "inserction_datetime": get_now(),
            "supplier_document": company_doc,
            "reference": "REFERER001",
            "store": 1
        })

        assert batch

        product = CreateProductV1(product_data={
            'batch': batch.pk,
            'price': 10,
            'discount_value': 1,
            'bar_code': '1234567891012',
            'name': 'foo name',
            'stock': 5,
            'item_type': 'foo type'
        }).start()

        product_repository.delete(product=product)

        product = product_repository.get(filters={'bar_code': '1234567891012'}, can_raises=False)

        assert not product

    def test_should_fail_when_havent_product(self, mocker):
        product_repository = ProductRepository(product_document=Product)

        with pytest.raises(MissingParam) as error:
            product_repository.delete(product=None)

        assert error.value.message == 'Product is required.'
