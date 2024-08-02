import os
from dotenv import load_dotenv

load_dotenv()

MONGO_HOST = os.getenv("MONGODB_HOST")
MONGO_USER = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_PASS = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
MONGO_DATABASE = os.getenv("MONGODB_DATABASE")
MONGO_PORT = os.getenv("MONGODB_PORT")
MONGO_AUTHENTICATION_SOURCE = os.getenv("MONGO_AUTHENTICATION_SOURCE")
MONGO_UUID_REPRESENTATION = os.getenv("MONGO_UUID_REPRESENTATION")
MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}"

TAGS_META_DATA = [
    {
        'name': 'batch',
        'description': 'Um lote funciona como um indentificador de um grupo de produtos que foram adquiridos ou produzidos em um mesmo momento.'
    },
    {
        'name': 'product',
        'description': 'Um produto é uma mercadoria ou serviço que é oferecido para venda.'
    }
]
