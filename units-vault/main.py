import connection # noqa
from fastapi import FastAPI
from constants import TAGS_META_DATA
from controllers.product_controller import router as product_router
from controllers.batch_controller import router as batch_router


app = FastAPI(
    swagger_ui_parameters={'syntaxHighlight.theme': 'obsidian'},
    openapi_tags=TAGS_META_DATA,
    # If you are viewing this, change the docs_url to otheer uuid4 with 50 characters
    docs_url='/9c86ffd5-b84e-4fd9-bb48-37c5f6912020'
)

app.include_router(product_router)
app.include_router(batch_router)


@app.get("/hello_world")
def hello_world():
    return {"Hello": "World"}
