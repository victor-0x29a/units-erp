import pytest
from datetime import timedelta
from documents import Store, Product, Batch
from utils.dates import get_now
from repositories import StoreRepository, ProductRepository, BatchRepository
from exceptions import MissingParam, MissingDoc, GreaterThanPrice, HasWithSameBatch, AlreadyExists
from ..fixture import mongo_connection # noqa: F401, E261
from ..__mocks__.constants import company_doc


class TestCreate:
    def test_should_create(self, mocker):
        store_repository = StoreRepository(store_document=Store)
        batch_repository = BatchRepository(batch_document=Batch)
        product_repository = ProductRepository(product_document=Product)

        store = store_repository.create(data={
            "unit": 1,
            "name": "Store 1"
        })

        assert store

        batch = batch_repository.create(data={
            "expiry_date": get_now() + timedelta(days=1),
            "inserction_datetime": get_now(),
            "supplier_document": company_doc,
            "reference": "REFERER001",
            "store": store.pk
        })

        assert batch

        product = product_repository.create(data={
            'batch': batch.pk,
            'price': 10,
            'discount_value': 1,
            'bar_code': '1234567891012',
            'name': 'foo name',
            'stock': 5,
            'item_type': 'foo type'
        })

        assert product
        assert product.price == 10.0

    def test_should_fails_when_discount_price_is_greater_than_price(self, mocker):
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

        with pytest.raises(GreaterThanPrice) as error:
            product_repository.create(data={
                'batch': batch.pk,
                'price': 10,
                'discount_value': 11,
                'bar_code': '1234567891012',
                'name': 'foo name',
                'stock': 5,
                'item_type': 'foo type'
            })

        assert error.value.message == 'The discount is greater than the price of the product.'

    def test_should_fails_when_already_exists_by_batch(self, mocker):
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

        product_repository.create(data={
            'batch': batch.pk,
            'price': 10,
            'discount_value': 1,
            'bar_code': '1234567891012',
            'name': 'foo name',
            'stock': 5,
            'item_type': 'foo type'
        })

        with pytest.raises(HasWithSameBatch) as error:
            product_repository.create(data={
                'batch': batch.pk,
                'price': 10,
                'discount_value': 1,
                'bar_code': '1234567891012',
                'name': 'foo name',
                'stock': 5,
                'item_type': 'foo type'
            })

        assert error.value.message == 'Already has product with the same batch.'

    def test_should_fail_when_already_exists_by_bar_code(self, mocker):
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

        secondary_batch = batch_repository.create(data={
            "expiry_date": get_now() + timedelta(days=1),
            "inserction_datetime": get_now(),
            "supplier_document": company_doc,
            "reference": "REFERER002",
            "store": 1
        })

        assert secondary_batch

        product_repository.create(data={
            'batch': batch.pk,
            'price': 10,
            'discount_value': 1,
            'bar_code': '1234567891012',
            'name': 'foo name',
            'stock': 5,
            'item_type': 'foo type'
        })

        with pytest.raises(AlreadyExists) as error:
            product_repository.create(data={
                'batch': secondary_batch.pk,
                'price': 10,
                'discount_value': 1,
                'bar_code': '1234567891012',
                'name': 'foo name',
                'stock': 5,
                'item_type': 'foo type'
            })

        assert error.value.message == 'Product already exists by bar code.'


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

        product_repository.create(data={
            'batch': batch.pk,
            'price': 10,
            'discount_value': 1,
            'bar_code': '1234567891012',
            'name': 'foo name',
            'stock': 5,
            'item_type': 'foo type'
        })

        product = product_repository.get(filter={'name': 'foo name'}, can_raises=False)

        assert product
        assert product.price == 10.0

    def test_should_fails_when_unexists(self, mocker):
        product_repository = ProductRepository(product_document=Product)

        with pytest.raises(MissingDoc) as error:
            product_repository.get(filter={
                'name': 'foo'
            })

        assert error.value.message == 'Product not found.'

    def test_should_not_fails_when_unexists_and_cant_raises(self, mocker):
        product_repository = ProductRepository(product_document=Product)

        product = product_repository.get(filter={
            'name': 'foo'
        }, can_raises=False)

        assert not product

    def test_should_fails_when_havent_filters(self, mocker):
        product_repository = ProductRepository(product_document=Product)

        with pytest.raises(MissingParam) as error:
            product_repository.get(filter=None)

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

        product = product_repository.create(data={
            'batch': batch.pk,
            'price': 10,
            'discount_value': 1,
            'bar_code': '1234567891012',
            'name': 'foo name',
            'stock': 5,
            'item_type': 'foo type'
        })

        product_repository.delete(product=product)

        product = product_repository.get(filter={'bar_code': '1234567891012'}, can_raises=False)

        assert not product

    def test_should_fail_when_havent_product(self, mocker):
        product_repository = ProductRepository(product_document=Product)

        with pytest.raises(MissingParam) as error:
            product_repository.delete(product=None)

        assert error.value.message == 'Product is required.'
