from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from macetoide.src.models.forms.base_models import RegisterForm
from models.entities.user import User
from repositories.user import instance as user_repository
from models.security.security import hash_password
from routers.auth import get_current_user

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/email")
def get_user_email(user: Annotated[User, Depends(get_current_user)]):
    return user.mail


@router.get("/username")
def get_user_username(user: Annotated[User, Depends(get_current_user)]):
    return user.username


@router.post("/update/username")
def update_username(
    old_username: str,
    new_username: str,
    user: Annotated[User, Depends(get_current_user)],
):
    return user_repository.update_user(user, "username", old_username, new_username)


@router.post("/update/password")
def update_password(
    old_password: str,
    new_password: str,
    user: Annotated[User, Depends(get_current_user)],
):
    return user_repository.update_user(
        user, "password", hash_password(old_password), hash_password(new_password)
    )


@router.post("/update/mail")
def update_mail(
    old_mail: str, new_mail: str, user: Annotated[User, Depends(get_current_user)]
):
    return user_repository.update_user(user, "mail", old_mail, new_mail)


@router.post("/delete")
def delete_user(user: Annotated[User, Depends(get_current_user)]):
    return user_repository.delete(user.id)


@router.post("/register")
def create_user(register_form: RegisterForm):
    if user_repository.validate_user(register_form.username):
        raise HTTPException(status_code=409, detail="Nombre de Usuario ya en uso.")
    register_form.password = hash_password(register_form.password)
    return user_repository.save(register_form.to_dict())
