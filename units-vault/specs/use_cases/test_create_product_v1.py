import pytest
from datetime import timedelta
from use_cases import CreateProductV1
from documents import Product, Batch
from ..fixture import mongo_connection # noqa: F401, E261
from .helpers.generate_object_id import generate_object_id
from utils.dates import get_now


class TestCreateProductUseCaseV1:
    def test_create_product(self, mocker):
        batch_reference = 'ref009'

        Batch(
            reference=batch_reference,
            supplier_document=batch_reference,
            inserction_datetime=get_now(),
            expiry_date=get_now() + timedelta(days=1)
        ).save().id

        data = {
            'batch': batch_reference,
            'price': 10,
            'discount_value': 1,
            'name': 'Foo',
            'stock': 10,
            'item_type': 'construction'
        }

        mocker.patch.object(Product, 'objects', return_value=None)

        mocker.patch.object(Product, 'save', return_value=True)

        product = CreateProductV1(
            product_data=data
        ).start()

        assert product

    def test_should_fail_when_discount_is_greater(self, mocker):
        data = {
            'batch': generate_object_id(),
            'price': 10,
            'discount_value': 11,
            'name': 'foo name',
            'stock': 4,
            'item_type': 'construction'
        }

        mocker.patch.object(Product, 'objects', return_value=None)

        mocker.patch.object(Product, 'save', return_value=True)

        try:
            CreateProductV1(
                product_data=data
            ).start()
        except Exception as e:
            assert 'discount' in str(e)

    def test_should_fail_when_have_with_same_batch(self, mocker):
        data = {
            'batch': generate_object_id(),
            'price': 10,
            'discount_value': 1,
            'name': 'foo test',
            'stock': 5,
            'item_type': 'foo type'
        }

        mocker.patch.object(Product, 'objects', return_value=True)

        mocker.patch.object(Product, 'save', return_value=True)

        try:
            CreateProductV1(
                product_data=data
            ).start()
        except Exception as e:
            assert 'batch' in str(e)

    def test_should_find_a_batch_when_batch_is_string(self, mocker):
        batch_reference = "ref123"

        created_batch_id = Batch(
            supplier_document="123123",
            reference=batch_reference,
            expiry_date=get_now() + timedelta(days=1),
            inserction_datetime=get_now()
        ).save().id

        data = {
            'batch': batch_reference,
            'price': 10,
            'discount_value': 1,
            'name': 'Foo product',
            'stock': 10,
            'item_type': 'Foo type'
        }

        product = CreateProductV1(
            product_data=data
        ).start()

        assert product.batch == created_batch_id

    def test_should_create_with_bar_code(self, mocker):
        data = {
            'batch': generate_object_id(),
            'price': 10,
            'discount_value': 1,
            'bar_code': '1234567891012',
            'name': 'foo name',
            'stock': 5,
            'item_type': 'foo type'
        }

        mocker.patch.object(Product, 'objects', return_value=None)

        mocker.patch.object(Product, 'save', return_value=True)

        product = CreateProductV1(
            product_data=data
        ).start()

        assert product

    def test_should_create_without_bar_code(self, mocker):
        data = {
            'batch': generate_object_id(),
            'price': 10,
            'discount_value': 1,
            'name': 'foo name',
            'stock': 10,
            'item_type': 'foo type'
        }

        mocker.patch.object(Product, 'objects', return_value=None)

        mocker.patch.object(Product, 'save', return_value=True)

        product = CreateProductV1(
            product_data=data
        ).start()

        assert product

    def test_should_fail_when_havent_batch(self, mocker):
        data = {
            'price': 10,
            'discount_value': 1,
            'name': 'foo name',
            'stock': 10,
            'item_type': 'foo type'
        }

        with pytest.raises(Exception) as error:
            CreateProductV1(
                product_data=data
            ).start()

        assert "Missing batch." == error.value.message
