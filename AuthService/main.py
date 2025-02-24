from fastapi import FastAPI
from pydantic import BaseModel
from api import auth, users, roles

app = FastAPI()

class TokenData(BaseModel):
    id: int

app.include_router(auth.router, tags=["auth"])
app.include_router(users.router, tags=["users"])
app.include_router(roles.router, tags=["roles"])