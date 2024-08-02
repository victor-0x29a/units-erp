import pytest


@pytest.fixture(autouse=True)
def mongo_connection():
    import mongomock
    from mongoengine import connect, disconnect
    disconnect()
    connect('mongoenginetest', host='mongodb://localhost', mongo_client_class=mongomock.MongoClient)
    yield
