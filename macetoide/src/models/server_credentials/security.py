import bcrypt
from fastapi import Request, HTTPException
from macetoide.src.models.database.database import database as db
from macetoide.src.models.entities.user import User


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def get_current_user(request: Request) -> User:
    user_id = request.cookies.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="No estás autenticado")

    user_data = db.get_by_id("user", int(user_id))
    if not user_data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return User(user_data["id"], user_data["username"], user_data["email"])
