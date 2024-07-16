import connection # noqa
from fastapi import FastAPI
from controllers.v1.product_controller import router as user_router
from controllers.v1.batch_controller import router as batch_router


app = FastAPI()

app.include_router(user_router)
app.include_router(batch_router)


@app.get("/hello_world")
def hello_world():
    return {"Hello": "World"}
