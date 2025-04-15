from fastapi import APIRouter, Response, HTTPException, Request
from datetime import datetime, timedelta, timezone
import jwt
from typing import Union

from models.entities.user import User
from models.entities.viewer_user import ViewerUser
from models.entities.admin_user import AdminUser
from models.forms.base_models import LoginForm
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


def create_token(user: ViewerUser | AdminUser):
    expiration = datetime.now(tz=timezone.utc) + timedelta(minutes=token_exp)
    payload = {"user_id": user.id, "exp": expiration.timestamp()}
    return jwt.encode(payload, secret_key, algorithm="HS256")


def get_current_user(request: Request) -> ViewerUser | AdminUser:
    token = request.cookies.get("token")
    if token is None:
        raise HTTPException(status_code=401, detail="Token no proporcionado")

    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

    user_data: User = user_repository.get_by_id(payload.get("user_id"))
    if not user_data:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    if user_data.admin_role:
        return AdminUser(
            user_data.id, user_data.username, user_data.mail, user_data.password
        )
    else:
        return ViewerUser(
            user_data.id, user_data.username, user_data.mail, user_data.password
        )


@router.post("/logout")
def logout(request: Request, response: Response):
    token = request.cookies.get("token")
    if token is None:
        raise HTTPException(status_code=401, detail="No hay sesión activa")

    response.delete_cookie("token")
    return {"message": "Sesión cerrada correctamente"}


@router.post("/token/refresh")
def refresh_token(request: Request, response: Response):
    token = request.cookies.get("token")
    if token is None:
        raise HTTPException(status_code=401, detail="Token no proporcionado")

    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401, detail="Token expirado, no se puede renovar"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

    user_data = user_repository.get_by_id(payload.get("user_id"))
    if not user_data:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    new_token = create_token(user_data)
    response.set_cookie("token", new_token)
    return {"message": "Token renovado correctamente"}
