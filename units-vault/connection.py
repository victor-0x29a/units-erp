from pymongo import MongoClient
from mongoengine import connect
from constants import (
    MONGO_URI, MONGO_DATABASE,
    MONGO_HOST, MONGO_PASS,
    MONGO_USER, MONGO_AUTHENTICATION_SOURCE,
    MONGO_UUID_REPRESENTATION
)


mongo_client = MongoClient(MONGO_URI)
connect(
    db=MONGO_DATABASE,
    host=MONGO_HOST,
    username=MONGO_USER,
    password=MONGO_PASS,
    authentication_source=MONGO_AUTHENTICATION_SOURCE,
    uuidRepresentation=MONGO_UUID_REPRESENTATION
)
