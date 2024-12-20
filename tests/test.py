import sys
import time
from datetime import datetime

sys.path.append("C:\\dev\\py\\temp-backend\\src")

from sqlalchemy import DateTime, String, func, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from database import engine


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


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

i1 = Item(name="n")
print("->", i1.created_at)

session.add(i1)


session.commit()
session.refresh(i1)
# print("->", i1.created_at)
# time.sleep(10)
# i1.name = "jack"
# session.commit()
session.close()
