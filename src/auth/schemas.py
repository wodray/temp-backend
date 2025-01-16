from pydantic import BaseModel, Field


class RegisterForm(BaseModel):
    """注册表单"""

    mobile: str = Field(pattern=r"1[3456789]\d{9}")
    password: str
    img_code_id: int
    img_code: int
