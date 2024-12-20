from typing import Annotated

from fastapi import Depends
from sqlalchemy import URL
from sqlmodel import Session, SQLModel, create_engine

from config import settings

url_object = URL.create(
    drivername="mysql",
    username=settings.db_user,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_database,
)


engine = create_engine(url_object, echo=settings.db_echo)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

if __name__ == "__main__":
    print(url_object.render_as_string(False))
