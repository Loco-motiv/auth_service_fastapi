import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

YANDEX_CONFIG = {
    "CLIENT_ID": os.getenv("YANDEX_CLIENT_ID"),
    "CLIENT_SECRET": os.getenv("YANDEX_CLIENT_SECRET"),
    "REDIRECT_URI": os.getenv("YANDEX_REDIRECT_URI")
}

JWT_CONFIG = {
    "SECRET_KEY": os.getenv("JWT_SECRET_KEY"),
    "ALGORITHM": os.getenv("JWT_ALGORITHM"),
    "ACCESS_TOKEN_EXPIRE_MINUTES": int(os.getenv("JWT_EXPIRES_IN_MINUTES")),
}