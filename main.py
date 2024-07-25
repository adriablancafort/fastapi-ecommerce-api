from fastapi import FastAPI
from routers import product
from database import create_db_and_tables

app = FastAPI()


app.include_router(product.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# python -m uvicorn main:app
