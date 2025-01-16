from typing import Annotated

import redis
from fastapi import Depends
from sqlalchemy import URL
from sqlmodel import Session, SQLModel, create_engine

from config import settings

url_object = URL.create(
    drivername="mysql",
    username=settings.mysql_user,
    password=settings.mysql_password,
    host=settings.mysql_host,
    port=settings.mysql_port,
    database=settings.mysql_database,
)


engine = create_engine(url_object, echo=settings.db_echo)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    password=settings.redis_password,
    db=0,
    protocol=3,
    decode_responses=True,
)
