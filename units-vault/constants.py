import os
from dotenv import load_dotenv

load_dotenv()

MONGO_HOST = os.getenv("MONGODB_HOST")
MONGO_USER = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_PASS = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
MONGO_DATABASE = os.getenv("MONGODB_DATABASE")
MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}"

# App context

PRODUCT_DATA_TYPES = {
    'for_sale': 'for_sale',
    'for_remove_sale': 'for_remove_sale',
    'for_disposal': 'for_disposal',
    'for_donation': 'for_donation',
    'for_internal_use': 'for_internal_use',
    'for_supplier_collect': 'for_supplier_collect',
}
