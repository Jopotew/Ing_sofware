import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "..")
sys.path.append(src_path)


from datetime import datetime, timedelta, timezone
from typing import Annotated


from exceptions.exceptions import (
    RepositoryError,
    UserNotFoundError,
    UserFieldValidationError,
    DatabaseOperationError,
    PotNotFoundError,
    LogDataFetchError,
    PlantSearchError,
)
import jwt
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    status,
    Response,
    Request,
)
from fastapi.responses import JSONResponse
from models.entities.user import User
from models.security.security import hash_password, verify_password
from macetoide.src.models.forms.base_models import LoginForm, RegisterForm

from repositories.user import instance as user_repository
from repositories.pot import instance as pot_repository
from repositories.log import instance as log_repository
from repositories.plant import instance as plant_repository


app = FastAPI()
app.title = "Macetoide API"
app.description = (
    "API for Macetoide, a platform for sharing and checking your macetoides."
)
app.version = "0.69"

secret_key = "opdiwfnpoiajqjuanpilocuraknaspjnpjasdnfbpjinmanoloeltronadordrakukeoelempaladorleinsertoeldedodiceporfavortkiosodvo"
token_exp = 3


"""
TODO:
    - TESTEAR LUEGO DE ESO
        FUNCIONES QUE FALTAN:
        - CREAR POT/ PLANT BASE MODEL
        - GET USERNAME


    - .... 3 DORITOS DESPUES
    - FIN BACK
    - EMPEZAR CON TEMA DE FRONTEND O SENSORES. DEPENDE CUAL SE QUIERA HACER PRIMERO 
"""


@app.exception_handler(UserNotFoundError)
@app.exception_handler(PotNotFoundError)
@app.exception_handler(LogDataFetchError)
@app.exception_handler(PlantSearchError)
async def not_found_handler(request: Request, exc: RepositoryError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(UserFieldValidationError)
async def validation_error_handler(request: Request, exc: UserFieldValidationError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(DatabaseOperationError)
async def db_error_handler(request: Request, exc: RepositoryError):
    return JSONResponse(status_code=500, content={"detail": str(exc)})


@app.get("/", tags=["Home"])
def home():
    return {"Retorno a Home"}


@app.post("/token", tags=["Auth"])
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
        raise HTTPException(
            status_code=401, detail="Token de autenticación no proporcionado"
        )

    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

    user_id = payload.get("user_id")
    user = user_repository.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    return user


@app.get("/user/email", tags=["User"])
def get_user_email(user: Annotated[User, Depends(get_current_user)]):
    return user.mail

@app.get("/user/username", tags=["User"])
def get_user_username(user: Annotated[User, Depends(get_current_user)]):
    return user.username


@app.get("/user/pots", tags=["Pots"])
def get_user_pots(user: Annotated[User, Depends(get_current_user)]):
    return pot_repository.get_user_pots(user)


@app.post("/user/pots", tags=["Pot"])
def save_pot(pot: dict, user: Annotated[User, Depends(get_current_user)]):
    if pot.get("id_user") != user.id:
        raise HTTPException(
            status_code=403, detail="No autorizado para guardar esta maceta"
        )
    return pot_repository.save(pot)


@app.get("/user/pots/pot", tags=["Pot"])
def get_pot_by_id(pot_dict: dict, user: Annotated[User, Depends(get_current_user)]):
    pot = pot_repository.create_obj(pot_dict)
    if pot.id_user != user.id:
        raise HTTPException(
            status_code=403, detail="No autorizado para acceder a esta maceta"
        )
    return pot_repository.get_by_id(pot.id)


@app.get("/user/pots/pot/plant", tags=["Plant"])
def get_plant_by_id(plant_dict: dict, user: Annotated[User, Depends(get_current_user)]):
    return plant_repository.get_by_id(plant_repository.create_obj(plant_dict).id)


@app.get("/plants", tags=["Plants"])
def get_all_plants(user: Annotated[User, Depends(get_current_user)]):
    return plant_repository.get_all()


@app.get("/user/pots/pot/logs/log", tags=["Log"])
def get_last_log(pot_dict: dict, user: Annotated[User, Depends(get_current_user)]):
    pot = pot_repository.create_obj(pot_dict)
    if pot.id_user != user.id:
        raise HTTPException(
            status_code=403, detail="No autorizado para acceder a esta maceta"
        )
    return log_repository.get_last_log(pot)


@app.get("/user/pots/pot/logs", tags=["Logs"])
def get_logs(pot_dict: dict, user: Annotated[User, Depends(get_current_user)]):
    pot = pot_repository.create_obj(pot_dict)
    if pot.id_user != user.id:
        raise HTTPException(
            status_code=403, detail="No autorizado para acceder a esta maceta"
        )
    return log_repository.get_logs(pot)


@app.post("/user/pots/pot/logs/log", tags=["Log"])
def save_log(log: dict, user: Annotated[User, Depends(get_current_user)]):
    if log.get("id_user") != user.id:
        raise HTTPException(
            status_code=403, detail="No autorizado para guardar este log"
        )
    return log_repository.save(log)


@app.post("/users/user/username", tags=["User"])
def update_username(
    old_username: str,
    new_username: str,
    user: Annotated[User, Depends(get_current_user)],
):
    return user_repository.update_user(user, "username", old_username, new_username)


@app.post("/users/user/password", tags=["User"])
def update_password(
    old_password: str,
    new_password: str,
    user: Annotated[User, Depends(get_current_user)],
):
    old_pw_hash = hash_password(old_password)
    new_pw_hash = hash_password(new_password)
    return user_repository.update_user(user, "password", old_pw_hash, new_pw_hash)


@app.post("/users/user/mail", tags=["User"])
def update_mail(
    old_mail: str, new_mail: str, user: Annotated[User, Depends(get_current_user)]
):
    return user_repository.update_user(user, "mail", old_mail, new_mail)


@app.post("/users/user/pots/pot/update", tags=["Pot"])
def update_pot(pot_dict: dict, user: Annotated[User, Depends(get_current_user)]):
    if pot_dict.get("id_user") != user.id:
        raise HTTPException(
            status_code=403, detail="No autorizado para modificar esta maceta"
        )
    return pot_repository.save(pot_dict)


@app.post("/users/user/pots/pot/delete", tags=["Pot"])
def delete_pot(pot_dict: dict, user: Annotated[User, Depends(get_current_user)]):
    if pot_dict.get("id_user") != user.id:
        raise HTTPException(
            status_code=403, detail="No autorizado para eliminar esta maceta"
        )
    return pot_repository.delete(pot_dict["id"])


@app.post("/users/user/delete", tags=["User"])
def delete_user(user: Annotated[User, Depends(get_current_user)]):
    return user_repository.delete(user.id)


@app.post("/users/", tags=["User"])
def create_user(register_form: RegisterForm):
    if user_repository.validate_user(register_form.username):
        raise HTTPException(status_code=409, detail="Nombre de Usuario ya en uso.")

    register_form.password = hash_password(register_form.password)
    u_d = register_form.to_dict()
    return user_repository.save(u_d)
