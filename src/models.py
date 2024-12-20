import enum
from datetime import datetime

from sqlmodel import Column, DateTime, Enum, Field, SmallInteger, SQLModel, text

SQLModel.metadata.naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_`%(constraint_name)s`",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class BaseModel(SQLModel):
    # 将默认值配置为None，可以在创建实例时不用手动填写该参数的值
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime, server_default=text("CURRENT_TIMESTAMP")),
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime,
            server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        ),
    )
    status: int = Field(default=1, sa_column=Column(SmallInteger))


class Sex(enum.Enum):
    male = 1
    female = 2
    unknown = 0


class UserInfo(BaseModel, table=True):
    __tablename__ = "user_info"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    nickname: str = Field(max_length=64)
    mobile: str = Field(max_length=16)
    avatar_url: str = Field(max_length=256)
    signature: str = Field(max_length=256)
    sex: Sex = Field(default=Sex.unknown, sa_column=Column(Enum(Sex)))
    birth_date: datetime
    role_id: int
    last_message_read_time: datetime


def add():
    now = datetime.now()
    # 增
    u1 = UserInfo(
        nickname="Jack",
        mobile="12345678",
        avatar_url="url",
        signature="qianming",
        birth_date=now,
        role_id=1,
        last_message_read_time=now,
    )

    print("->", u1)
    with Session(engine) as session:
        session.add(u1)
        session.commit()
        session.refresh(u1)
        print("->", u1)


def query():
    with Session(engine) as session:
        statement = (
            select(UserInfo)
            .where(or_(UserInfo.nickname == "jack", UserInfo.nickname == "rose"))
            .where(col(UserInfo.id) < 100)
        )
        results = session.exec(statement)
        # users = results.all()
        for u in results:
            print("->", u)


if __name__ == "__main__":
    from sqlmodel import Session, col, or_, select

    from database import engine
