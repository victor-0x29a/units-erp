import connection # noqa
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
import fastapi_error_handler
from constants import TAGS_META_DATA
from controllers.v1.product_controller import router as product_router_v1
from controllers.v1.batch_controller import router as batch_router_v1
from controllers.v1.store_controller import router as store_router_v1
from controllers.v1.employee_controller import router as employee_router_v1


app = FastAPI(
    swagger_ui_parameters={'syntaxHighlight.theme': 'obsidian'},
    openapi_tags=TAGS_META_DATA,
    # If you are viewing this, change the docs_url to other uuid4 with 50 characters
    docs_url='/9c86ffd5-b84e-4fd9-bb48-37c5f6912020'
)

app.add_exception_handler(RequestValidationError, fastapi_error_handler.http_exceptions)
app.add_exception_handler(Exception, fastapi_error_handler.unhandled_exceptions)

app.include_router(product_router_v1)
app.include_router(batch_router_v1)
app.include_router(store_router_v1)
app.include_router(employee_router_v1)


@app.get("/hello_world")
def hello_world():
    return {"Hello": "World"}
