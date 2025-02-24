from pydantic import BaseModel

class PhoneInfo(BaseModel):
    id: int
    number: str

class YandexUserInfo(BaseModel):
    id: int
    display_name: str
    default_phone: PhoneInfo | None = None

class User(BaseModel):
    id: int
    username: str
    role: str
