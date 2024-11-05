import pytest
from datetime import timedelta
from bson import ObjectId
from mongoengine.queryset import QuerySet
from use_cases import CreateProductV1
from documents import Product, Batch
from exceptions import MissingDoc, UniqueKey
from ..fixture import mongo_connection # noqa: F401, E261
from .helpers.generate_object_id import generate_object_id
from utils.dates import get_now


class TestCreateProductUseCaseV1:
    def test_create_product(self, mocker):
        batch_reference = 'ref009'

        Batch(
            reference=batch_reference,
            supplier_document='04.954.588/0001-73',
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

        with pytest.raises(Exception) as error:
            CreateProductV1(
                product_data=data
            ).start()

        assert 'discount' in str(error)

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

        with pytest.raises(Exception) as error:
            CreateProductV1(
                product_data=data
            ).start()

        assert 'batch' in str(error)

    def test_should_find_a_batch_when_batch_is_string(self, mocker):
        batch_reference = "ref123"

        created_batch_id = Batch(
            supplier_document="76.099.428/0001-03",
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

        assert error.value.message == "Missing batch."

    def test_should_fail_when_doesnt_find_batch(self, mocker):
        data = {
            'batch': str(ObjectId()),
            'price': 10,
            'discount_value': 1,
            'name': 'foo name',
            'stock': 10,
            'item_type': 'foo type'
        }

        mocker.patch.object(QuerySet, 'get', side_effect=MissingDoc('Batch not found.'))

        with pytest.raises(Exception) as error:
            CreateProductV1(
                product_data=data
            ).start()

        assert error.value.message == "Batch not found."

    def test_should_fail_when_already_exists_other_by_bar_code(self, mocker):
        data = {
            'batch': generate_object_id(),
            'price': 10,
            'discount_value': 1,
            'name': 'foo name',
            'stock': 10,
            'item_type': 'foo type',
            'bar_code': '1234567891012'
        }

        CreateProductV1(
            product_data=data
        ).start()

        data = {
            'batch': generate_object_id(),
            'price': 10,
            'discount_value': 1,
            'name': 'foo name',
            'stock': 10,
            'item_type': 'foo type',
            'bar_code': '1234567891012'
        }

        with pytest.raises(UniqueKey) as error:
            CreateProductV1(
                product_data=data
            ).start()

        assert error.value.message == 'Product with same bar code already exists.'
