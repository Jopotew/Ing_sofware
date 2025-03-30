import bcrypt
from fastapi import Request, HTTPException
import jwt
import os
from dotenv import load_dotenv

# from macetoide.src.models.database.database import database as db
#from macetoide.src.models.entities.user import User



load_dotenv()
secret_key = os.getenv("SECRET_JWT_KEY")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def create_token(user: dict):
    payload = {"user_id": user["id"]}
    token_jwt = jwt.encode(payload, secret_key, algorithm="HS256")
    return token_jwt


def get_current_user(request: Request):
    token = request.cookies.get("token")

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se proporcionó un token de autenticación",
        )

    payload = jwt.decode(token, secret_key, algorithms=["HS256"])

    if payload["exp"] < datetime.now(tz=timezone.utc).timestamp():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, #FRONT SI SE RECIBE ESTA U OTRAS EXCEPCIONES SE DEBE VOLVERT A LA PAGINA ACORDE.
            detail="Token expirado",
        )

    user_id = payload.get("user_id", None)
    user = users["pablo"]  # user_repository.get_user_by_id(user_id)
    return user