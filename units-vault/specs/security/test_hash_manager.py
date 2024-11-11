from security import HashManager


class TestHashManager:
    def test_should_create(self, mocker):
        raw_content = 'hello there!'

        hash_manager = HashManager()

        hashed = hash_manager.hash_passwd(content=raw_content)

        assert hashed
        assert raw_content != hashed

    def test_should_is_not_equal(self, mocker):
        raw_content_1 = 'hello there!'

        raw_content_2 = 'hello there'

        hash_manager = HashManager()

        hashed_content_1 = hash_manager.hash_passwd(content=raw_content_1)

        hashed_content_2 = hash_manager.hash_passwd(content=raw_content_2)

        assert hashed_content_1 != hashed_content_2

    def test_should_is_not_equal_by_salts(self, mocker):
        raw_content_1 = 'hello there!'

        raw_content_2 = 'hello there!'

        hash_manager = HashManager()

        hashed_content_1 = hash_manager.hash_passwd(content=raw_content_1)

        hashed_content_2 = hash_manager.hash_passwd(content=raw_content_2)

        assert hashed_content_1 != hashed_content_2
