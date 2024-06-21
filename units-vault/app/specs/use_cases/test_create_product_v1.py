from use_cases import CreateProductV1


class TestCreateProductUseCaseV1:
    def test_create_product(self, mocker):
        data = {
            'batch': '123',
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

        assert product

    def test_should_fail_when_discount_is_greater(self, mocker):
        data = {
            'batch': '123',
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
            'batch': '123',
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
