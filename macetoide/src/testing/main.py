import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "..")
sys.path.append(src_path)


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
from models.entities.user import User
from models.server_credentials.security import (
    hash_password,
    verify_password,
)

from repositorys.user import instance as user_repository
from repositorys.pot import instance as pot_repository
from repositorys.log import instance as log_repository
from repositorys.plant import instance as plant_repository


from models.server_credentials.auth import LoginForm


app = FastAPI()


app.title = "Macetoide API"
app.description = (
    "API for Macetoide, a platform for sharing and checking your macetoides."
)
app.version = "0.69"

secret_key = "opdiwfnpoiajqjuanpilocuraknaspjnpjasdnfbpjinmanoloeltronadordrakukeoelempaladorleinsertoeldedodiceporfavortkiosodvo"
token_exp = 3


@app.get("/", tags=["Home"])
def home():
    return {"Retorno a Home"}

#Modificar entidades para q tamb exista BASEMODEL en si, esas son las que se usn en las func. 

@app.post("/token", tags=["Auth"])
def login(response: Response, login_form: LoginForm):
    user = user_repository.get_by_username(login_form.username)
    print(user)
    if user is None:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    if not verify_password(login_form.password, user.password):
        print("USER IN DB PW",user.password)
        print("USER IN LOGIN FORM PW",login_form.password)
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = create_token(user)
    response.set_cookie("token", token)

    return "Login Succesful! Welcome", user.username


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



@app.get("/user/email", tags=["User"])
def get_user_email(user: Annotated[User, Depends(get_current_user)]):
    return user.mail



@app.get("/user/pots", tags=["Pots"])
def get_user_pots(user: Annotated[User,Depends(get_current_user)]):
    if user:
        pots = pot_repository.get_pots(user.id)
        return pots
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@app.post("/user/pots", tags=["Pots"])
def save_pot(pot: dict, user: Annotated[User,Depends(get_current_user)]):
    if user:
        st = pot_repository.save_pot(pot)
        if st:
            return st
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@app.get("/user/pots/pot", tags=["Pot"])
def get_pot_by_id(pot_id: dict, user: Annotated[User,Depends(get_current_user)]):
    if user:
        id = pot_id["pot_id"]
        return pot_repository.get_by_id(id)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@app.get("/user/pots/pot/plants/plant", tags=["Plant"])
def get_plant_by_id(plant_id: dict, user: Annotated[User,Depends(get_current_user)]):
    if user:
        id = plant_id["plant_id"]
        return plant_repository.get_by_id(plant_id)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    

@app.get("/plants", tags=["Plants"])
def get_plants(user: Annotated[User,Depends(get_current_user)]):
    if user:
        return plant_repository.get_all()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@app.get("/user/pots/pot/logs/log", tags=["Log"])
def get_last_log(pot_dict: dict, user: Annotated[User,Depends(get_current_user)]):
    if user:
        pot = pot_repository.create_pot(pot_dict)
        return log_repository.get_last_log(pot)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@app.get("/user/pots/pot/logs", tags=["Logs"])
def get_logs(pot_dict : dict , user: Annotated[User,Depends(get_current_user)]):
    if user:
        pot = pot_repository.create_pot(pot_dict)
        return log_repository.get_logs(pot)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@app.get("/user/pots/pot/logs/log", tags=["Log"])
def save_log(log: dict):

    st = log_repository.save(log)
    if st:
        return st
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.post("/users/user", tags=["User"])
def update_username(old_username: str, new_username, user: Annotated[User,Depends(get_current_user)]):
    if user:
        st = user_repository.update_user(user.id, "username", old_username, new_username)
        if st:
            return st
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
@app.post("/users/user", tags=["User"])
def update_password(old_password: str, new_password: str, user: Annotated[User,Depends(get_current_user)]):
    if user:
        old_pw_hash = hash_password(old_password)
        new_pw_hash = hash_password(new_password)
        st = user_repository.update_user(user.id, "password", old_pw_hash, new_pw_hash)
        if st:
            return st
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    


@app.post("/users/user", tags=["User"])
def update_mail(old_mail: str, new_mail: str, user: Annotated[User,Depends(get_current_user)]):
    if user:

        st = user_repository.update_user(user.id, "mail", old_mail, new_mail)
        if st:
            return st
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

#modificar y elimnar pots
@app.post("/users/user/pots/pot", tags=["Pot"])
def delete_pot(pot_dict: dict, user: Annotated[User,Depends(get_current_user)]):
    if user:
        st = pot_repository.delete(pot_dict["id"])
        if st:
            return st
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)     

@app.post("/users/user", tags=["User"])
def delete_user(user: Annotated[User,Depends(get_current_user)]):
    if user:
        st = pot_repository.delete(user.id)
        if st:
            return st
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) 



#FALTA LA VALIDACION DE QUE YA EXISTE UN USUARIO EN LA DB.


@app.post("/users/", tags=["User"])
def create_user(user: dict):
    if "password" in user:
        user["password"] = hash_password(user["password"])
    st = user_repository.save(user)
    if st:
        return st
    else:
        raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail="No se pudo crear el usuario")

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
