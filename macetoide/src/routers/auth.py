from fastapi import APIRouter, Response, HTTPException, Request
from datetime import datetime, timedelta, timezone
import jwt

from macetoide.src.models.entities.user import User
from macetoide.src.models.forms.base_models import LoginForm
from models.security.security import verify_password
from repositories.user import instance as user_repository

router = APIRouter(tags=["Auth"])

secret_key = "opdiwfnpoiajqjuanpilocuraknaspjnpjasdnfbpjinmanoloeltronadordrakukeoelempaladorleinsertoeldedodiceporfavortkiosodvo"
token_exp = 3


@router.post("/token")
def login(response: Response, login_form: LoginForm):
    user = user_repository.get_by_username(login_form.username)
    if user is None or not verify_password(login_form.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = create_token(user)
    response.set_cookie("token", token)
    return "Login Succesful! Welcome", user.username


def create_token(user: User):
    expiration = datetime.now(tz=timezone.utc) + timedelta(minutes=token_exp)
    payload = {"user_id": user.id, "exp": expiration.timestamp()}
    return jwt.encode(payload, secret_key, algorithm="HS256")


def get_current_user(request: Request):
    token = request.cookies.get("token")
    if token is None:
        raise HTTPException(status_code=401, detail="Token no proporcionado")

    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = user_repository.get_by_id(payload.get("user_id"))
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user
