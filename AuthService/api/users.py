from typing import Annotated  
from fastapi import APIRouter, Depends
from db.postgresql import get_user_history
from models.user import User
from services.auth import get_current_user

router = APIRouter()

@router.get("/me/")
async def get_me(user: Annotated[User, Depends(get_current_user)]):
    return user

@router.get("/history/")
async def get_history(user: Annotated[User, Depends(get_current_user)]):
    history = await get_user_history(user["id"])
    return history