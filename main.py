from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import product
from database import create_db_and_tables

app = FastAPI()


origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(product.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# python -m uvicorn main:app
