from datetime import datetime

from sqlalchemy import DateTime, String, create_engine, func, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=256), nullable=False)
    price: Mapped[float] = mapped_column(server_default="0")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        server_default=text("ON UPDATE CURRENT_TIMESTAMP"),
    )


engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
# Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
# session = Session()

# i1 = Item(name="n")
# print("->", i1.created_at)

# session.add(i1)


# session.commit()
# session.refresh(i1)
# print("->", i1.created_at)
# time.sleep(10)
# i1.name = "jack"
# session.commit()
# session.close()

if __name__ == "__main__":
    import uuid

    from pydantic import BaseModel, ConfigDict
    from sqlmodel import Field, SQLModel

    class Hero(SQLModel, table=True):
        id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
        name: str = Field(index=True)
        secret_name: str
        age: int | None = Field(default=None, index=True)
        last_login: datetime = Field(default_factory=datetime.now)

    h = Hero(name="", secret_name="")

    print(h)
