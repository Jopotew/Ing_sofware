from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import (
    Body,
    Depends,
    FastAPI,
    HTTPException,
    Query,
    status,
    Response,
    Request,
)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel


from macetoide.src.models.server_credentials.security import (
    hash_password,
    verify_password,
)

from macetoide.src.repositorys.user import instance as user_repository

# from macetoide.src.repositorys.pot import instance as pot_repository
# from macetoide.src.repositorys.log import instance as log_repository
# from macetoide.src.repositorys.plant import instance as plant_repository
# from macetoide.src.models.server_credentials.security import get_current_user

from macetoide.src.models.server_credentials.auth import LoginForm

# from macetoide.src.models.entities.user import User
# from macetoide.src.models.entities.pot import Pot
# from macetoide.src.models.entities.plant import Plant


app = FastAPI()


app.title = "Macetoide API"
app.description = (
    "API for Macetoide, a platform for sharing and checking your macetoides."
)
app.version = "0.0.1"

secret_key = "opdiwfnpoiajqjuanpilocuraknaspjnpjasdnfbpjinmanoloeltronadordrakukeoelempaladorleinsertoeldedodiceporfavortkiosodvo"
token_exp = 3


@app.get("/", tags=["Home"])
def home():
    return {"Retorno a Home"}


@app.post("/token", tags=["Auth"])
def login(response: Response, login_form: LoginForm):
    user = user_repository.get_by_username(login_form.username)

    if user is None:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    if not verify_password(login_form.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = create_token(user)
    response.set_cookie("token", token)

    return "Success!"


def create_token(user):
    expiration = datetime.now(tz=timezone.utc) + timedelta(minutes=token_exp)
    payload = {"user_id": user.id, "exp": expiration.timestamp()}
    token_jwt = jwt.encode(payload, secret_key, algorithm="HS256")
    return token_jwt


def get_current_user(request: Request):
    token = request.cookies.get("token")

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se proporcionó un token de autenticación",
        )

    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )

    user_id = payload.get("user_id")
    user_dict = user_repository.get_by_id(user_id)
    user = user_repository.create_user(user_dict)
    return user


#    

# @app.get("/user/email", tags=["Auth"])
# def get_user_email(user: Annotated[dict, Depends(get_current_user)]):
#     return user["email"]


# def common_parameters(id: str, edad: int, nombre: str) -> dict:
#     return { "id": id, "edad": edad, "nombre": nombre}

# @app.get("/ajksdksjd", tags=["Auth"])
# def get_algo(persona: Annotated[dict, Depends(common_parameters)]):
#     return persona

# @app.get("/ajksdksjd2", tags=["Auth"])
# def get_algo2(persona: Annotated[dict, Depends(common_parameters)], nombre_padre: Annotated[str, Query()]):
#     return persona


# @app.post("/login", tags=["Auth"])
# def login(data: LoginRequest, response: Response):

#     user: User = user_repository.verify_user(data.username, data.password)
#     if not user:
#         raise HTTPException(status_code=401, detail="Credenciales incorrectas")

#     response.set_cookie(key="user_id", value=str(user.id), httponly=True)
#     return {"message": "Login exitoso"}


# @app.get("/pots/", tags=["Pots"])
# def get_user_pots(user: User = Depends(get_current_user)):
#     return user_repository.get_pots(user.id)


# @app.post("/users/{user_id}/pots/", tags=["Pots"])
# def add_new_pot(
#     user_id: int,
# ):
#     """
#     Agrega una maceta a un usuario donde el id de la maceta es el id del usuario
#     1)checkear si el user id existe y esta logeado, mandando la request
#     2)checkear si el pot id existe, y pertenece al user
#     """
#     user = user_repository.get_by_id(user_id)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")

#     pot = create_pot()

#     if pot.user != user:
#         raise HTTPException(status_code=403, detail="Pot does not belong to user")

#     user.add_pot(pot)
#     return pot.get_dto()


# @app.get("/users/{user_id}/pots/{pot_id}", tags=["Pots"])
# def get_pot(user_id: int, pot_id: int):
#     user = user_repository.get_by_id(user_id)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")

#     pot = pot_repository.get_by_id(pot_id)
#     if pot is None:
#         raise HTTPException(status_code=404, detail="Pot not found")

#     if pot.user != user:
#         raise HTTPException(status_code=403, detail="Pot does not belong to user")

#     return pot.get_dto()
