from use_cases import CreateHashV1


class TestCreateHashUseCaseV1:
    def test_should_create(self, mocker):
        raw_content = 'hello there!'

        create_hash = CreateHashV1()

        hashed = create_hash.hash_passwd(content=raw_content)

        assert hashed
        assert raw_content != hashed

    def test_should_is_not_equal(self, mocker):
        raw_content_1 = 'hello there!'

        raw_content_2 = 'hello there'

        create_hash = CreateHashV1()

        hashed_content_1 = create_hash.hash_passwd(content=raw_content_1)

        hashed_content_2 = create_hash.hash_passwd(content=raw_content_2)

        assert hashed_content_1 != hashed_content_2

    def test_should_is_not_equal_by_salts(self, mocker):
        raw_content_1 = 'hello there!'

        raw_content_2 = 'hello there!'

        create_hash = CreateHashV1()

        hashed_content_1 = create_hash.hash_passwd(content=raw_content_1)

        hashed_content_2 = create_hash.hash_passwd(content=raw_content_2)

        assert hashed_content_1 != hashed_content_2
