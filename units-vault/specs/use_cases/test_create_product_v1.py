from use_cases import CreateProductV1
from .helpers.generate_object_id import generate_object_id


class TestCreateProductUseCaseV1:
    def test_create_product(self, mocker):
        data = {
            'batch': generate_object_id(),
            'price': 10,
            'discount_value': 1
        }

        mock_product = mocker.patch('documents.Product')

        mocker.patch.object(mock_product, 'objects', return_value=None)

        mocker.patch.object(mock_product, 'save', return_value=True)

        product = CreateProductV1(
            product_document=mock_product,
            product_data=data
        ).start()

        assert product[0]

        assert product[1] == data

    def test_should_fail_when_discount_is_greater(self, mocker):
        data = {
            'batch': generate_object_id(),
            'price': 10,
            'discount_value': 11
        }

        mock_product = mocker.patch('documents.Product')

        mocker.patch.object(mock_product, 'objects', return_value=None)

        mocker.patch.object(mock_product, 'save', return_value=True)

        try:
            CreateProductV1(
                product_document=mock_product,
                product_data=data
            ).start()
        except Exception as e:
            assert 'discount' in str(e)

    def test_should_fail_when_have_with_same_batch(self, mocker):
        data = {
            'batch': generate_object_id(),
            'price': 10,
            'discount_value': 1
        }

        mock_product = mocker.patch('documents.Product')

        mocker.patch.object(mock_product, 'objects', return_value=True)

        mocker.patch.object(mock_product, 'save', return_value=True)

        try:
            CreateProductV1(
                product_document=mock_product,
                product_data=data
            ).start()
        except Exception as e:
            assert 'batch' in str(e)

    def test_should_find_a_batch_when_batch_is_string(self, mocker):
        data = {
            'batch': '123123',
            'price': 10,
            'discount_value': 1
        }

        obj_id = generate_object_id()

        mock_product_cls = mocker.MagicMock()

        mock_batch_cls = mocker.MagicMock()

        mock_batch_cls.objects.get.return_value.id = obj_id

        mock_product_cls.objects.return_value = None

        product = CreateProductV1(
            product_document=mock_product_cls,
            batch_document=mock_batch_cls,
            product_data=data
        ).start()

        assert product[1].get('batch') == obj_id

    def test_should_create_with_bar_code(self, mocker):
        data = {
            'batch': generate_object_id(),
            'price': 10,
            'discount_value': 1,
            'bar_code': '123456789012'
        }

        mock_product = mocker.patch('documents.Product')

        mocker.patch.object(mock_product, 'objects', return_value=None)

        mocker.patch.object(mock_product, 'save', return_value=True)

        product = CreateProductV1(
            product_document=mock_product,
            product_data=data
        ).start()

        assert product[0]

        assert product[1] == data

    def test_should_create_without_bar_code(self, mocker):
        data = {
            'batch': generate_object_id(),
            'price': 10,
            'discount_value': 1
        }

        mock_product = mocker.patch('documents.Product')

        mocker.patch.object(mock_product, 'objects', return_value=None)

        mocker.patch.object(mock_product, 'save', return_value=True)

        product = CreateProductV1(
            product_document=mock_product,
            product_data=data
        ).start()

        assert product[0]

        assert product[1] == data
