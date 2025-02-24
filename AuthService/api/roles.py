from fastapi import APIRouter
from db.postgresql import get_roles

router = APIRouter()

@router.get("/roles/")
async def get_roles_handler():
    roles = await get_roles()
    return {"roles": roles}