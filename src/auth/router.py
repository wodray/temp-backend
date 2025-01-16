from typing import Annotated

from fastapi import APIRouter, Form

from ..database import SessionDep
from ..users.models import UserInfo, UserLogin
from .schemas import RegisterForm
from .utils import get_password_hash

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def user_register(session: SessionDep, form: Annotated[RegisterForm, Form()]):
    password_hash = get_password_hash(form.password)

    user_info = UserInfo(mobile=form.mobile, nickname=form.mobile)
    session.add(user_info)

    user_login = UserLogin(
        mobile=form.mobile, password_hash=password_hash, user_id=user_info.id
    )

    session.add(user_login)
    session.commit()
