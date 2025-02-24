from datetime import datetime, timedelta
from fastapi import Depends
from fastapi.security import APIKeyCookie
import httpx
from db.postgresql import get_user_by_id, add_user, add_login_time
from services.jwt import verify_token
from models.user import User, YandexUserInfo
from exceptions import InvalidCredentialsException
from settings import JWT_CONFIG
from services.jwt import create_token
from confluent_kafka import Producer


cookie_scheme = APIKeyCookie(name="users_access_token")

def publish_to_kafka(user_info):
    conf = {'bootstrap.servers': 'kafka:9092'}
    producer = Producer(conf)
    producer.produce('user-registered', json.dumps({
        'id': user_info.id,
        'username': user_info.display_name
    }))
    producer.flush()

async def get_current_user(token: str = Depends(cookie_scheme)) -> User:
    user_id = verify_token(token)
    return await get_user_by_id(user_id)

async def get_yandex_user_info(access_token: str) -> YandexUserInfo:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://login.yandex.ru/info",
            headers={"Authorization": f"OAuth {access_token}"},
        )
        if response.status_code != 200:
            raise InvalidCredentialsException
        user_info = response.json()
        return YandexUserInfo(**user_info)
    
async def set_access_cookie(response, yandex_response):
    if yandex_response.status_code != 200:
            raise InvalidCredentialsException
    token_data = yandex_response.json()
    access_token = token_data["access_token"]
    user_info = await get_yandex_user_info(access_token)

    user = await get_user_by_id(user_info.id)
    if not user:
        user = await add_user(user_info.id, user_info.display_name, "user")
    await add_login_time(user_info.id, datetime.now())

    jwt_access_token = create_token({"sub": str(user_info.id)}, timedelta(minutes=JWT_CONFIG["ACCESS_TOKEN_EXPIRE_MINUTES"]))
    response.set_cookie(key="users_access_token", value=jwt_access_token, httponly=True)

    return jwt_access_token