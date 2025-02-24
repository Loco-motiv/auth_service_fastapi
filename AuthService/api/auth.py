from fastapi import APIRouter, Response
from fastapi.responses import RedirectResponse
import httpx
from settings import YANDEX_CONFIG
from services.auth import set_access_cookie

router = APIRouter()

@router.get("/login/yandex")
async def login_yandex():
    auth_url = f"https://oauth.yandex.ru/authorize?response_type=code&client_id={YANDEX_CONFIG['CLIENT_ID']}&redirect_uri={YANDEX_CONFIG['REDIRECT_URI']}"
    return RedirectResponse(url=auth_url)

@router.get("/auth/yandex/callback")
async def auth_yandex_callback(response: Response, code: str):
    async with httpx.AsyncClient() as client:
        yandex_response = await client.post(
            "https://oauth.yandex.ru/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": YANDEX_CONFIG["CLIENT_ID"],
                "client_secret": YANDEX_CONFIG["CLIENT_SECRET"],
                "redirect_uri": YANDEX_CONFIG["REDIRECT_URI"],
            },
        )

        jwt_access_token = await set_access_cookie(response, yandex_response)

        return jwt_access_token