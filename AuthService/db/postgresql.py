import asyncpg
from datetime import datetime
from settings import DB_CONFIG

async def add_user(user_id: int, user_name: str, role: str):
    query = "INSERT INTO users (id, username, role_id) VALUES ($1::INTEGER, $2::TEXT, (SELECT id FROM roles WHERE name = $3::TEXT));"

    conn = await asyncpg.connect(**DB_CONFIG)
    
    try:
        await conn.execute(query, user_id, user_name, role)
    finally:
        await conn.close()

async def get_user_by_id(user_id: int):
    query = "SELECT users.id as id, username, name as role FROM users JOIN roles on (users.role_id = roles.id) WHERE users.id = $1::INTEGER;"
    
    conn = await asyncpg.connect(**DB_CONFIG)
    
    try:
        row = await conn.fetchrow(query, int(user_id))
        if not row:
            return None
        return dict(row)
    finally:
        await conn.close()

async def add_login_time(user_id: int, datetime: datetime):
    query = "INSERT INTO history (user_id, login_at) VALUES ($1::INTEGER, $2::TIMESTAMP);"
    
    conn = await asyncpg.connect(**DB_CONFIG)
    
    try:
        await conn.execute(query, user_id, datetime)
    finally:
        await conn.close()

async def change_user_role(user_id: int, role: str):
    query = "UPDATE users SET role_id = (SELECT id FROM roles WHERE name = $2::TEXT) WHERE id = $1::INTEGER;"
    
    conn = await asyncpg.connect(**DB_CONFIG)
    
    try:
        await conn.execute(query, user_id, role)
    finally:
        await conn.close()

async def get_user_history(user_id: int):
    query = "SELECT * FROM history WHERE user_id = $1::INTEGER;"

    conn = await asyncpg.connect(**DB_CONFIG)

    try:
        rows = await conn.fetch(query, user_id)
        return [dict(row) for row in rows]
    finally:
        await conn.close()

async def get_roles():
    query = "SELECT * FROM roles;"

    conn = await asyncpg.connect(**DB_CONFIG)

    try:
        rows = await conn.fetch(query)
        return [dict(row) for row in rows]
    finally:
        await conn.close()

async def get_history():
    query = "SELECT * FROM history;"

    conn = await asyncpg.connect(**DB_CONFIG)

    try:
        rows = await conn.fetch(query)
        return [dict(row) for row in rows]
    finally:
        await conn.close()