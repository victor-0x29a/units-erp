from fastapi import FastAPI
from controllers.product_controller import router as user_router

app = FastAPI()

app.include_router(user_router)


@app.get("/hello_world")
def hello_world():
    return {"Hello": "World"}
