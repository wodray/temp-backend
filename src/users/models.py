import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, SmallInteger, text
from sqlmodel import Field, SQLModel


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


class UserLogin(BaseModel, table=True):
    """用户登录表"""

    __tablename__ = "user_login"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)  # 用户id
    mobile: str = Field(max_length=16, unique=True, nullable=False)
    password_hash: str = Field(max_length=128, nullable=False)
    user_id: int  # 用户id
    last_login: datetime = Field(default_factory=datetime.now)  # 最后一次登录时间
    last_login_stamp: int  # 最后一次登录时间


class Sex(enum.Enum):
    male = 1
    female = 2
    unknown = 0


class UserInfo(BaseModel, table=True):
    """用户信息表"""

    __tablename__ = "user_info"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    nickname: str = Field(max_length=64)
    mobile: str = Field(max_length=16)
    avatar_url: str | None = Field(default=None, max_length=256)
    signature: str | None = Field(default=None, max_length=256)
    sex: Sex = Field(default=Sex.unknown, sa_column=Column(Enum(Sex)))
    birth_date: datetime | None = Field(default=None)
    role_id: int | None
    is_admin: int = Field(default=0, sa_column=Column(SmallInteger))
    last_message_read_time: datetime
