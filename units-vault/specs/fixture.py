import pytest
import mongomock
from mongoengine import connect, disconnect


@pytest.fixture(autouse=True)
def mongo_connection():
    disconnect()
    connect(
        'mongoenginetest',
        host='mongodb://localhost',
        mongo_client_class=mongomock.MongoClient,
        uuidRepresentation='standard'
    )
    yield
