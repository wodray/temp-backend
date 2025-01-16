from contextlib import asynccontextmanager

from fastapi import FastAPI

from auth.router import router
from config import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("startup")
    # startup
    yield
    # shutdown
    logger.info("shutdown")


app = FastAPI(lifespan=lifespan)
app.include_router(router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
