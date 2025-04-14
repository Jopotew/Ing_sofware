from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from models.forms.base_models import DataUpdateForm, RegisterForm
from models.entities.viewer_user import ViewerUser
from models.entities.admin_user import AdminUser
from repositories.user import instance as user_repository
from models.security.security import hash_password
from routers.auth import get_current_user

router = APIRouter(prefix="/user", tags=["User"])



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~VIEWER~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

@router.get("/email")
def get_user_email(user: Annotated[ViewerUser, Depends(get_current_user)]):
    return user.mail


@router.get("/username")
def get_user_username(user: Annotated[ViewerUser, Depends(get_current_user)]):
    return user.username


@router.post("/update/username")
def update_username(
    user: Annotated[ViewerUser, Depends(get_current_user)],
    body: DataUpdateForm
):
    return user_repository.update_user(user, "username", body.old_data, body.new_data)


@router.post("/update/password")
def update_password(
    user: Annotated[ViewerUser, Depends(get_current_user)],
    body: DataUpdateForm
):
    return user_repository.update_user(
        user,
        "password",
        hash_password(body.old_data),
        hash_password(body.new_data)
    )


@router.post("/update/mail")
def update_mail(
    user: Annotated[ViewerUser, Depends(get_current_user)],
    body: DataUpdateForm
):
    return user_repository.update_user(user, "mail", body.old_data, body.new_data)


@router.post("/delete")
def delete_user(user: Annotated[ViewerUser, Depends(get_current_user)]):
    return user_repository.delete(user.id)


@router.post("/register")
def create_user(register_form: RegisterForm):
    if user_repository.validate_user(register_form.username):
        raise HTTPException(status_code=409, detail="Nombre de Usuario ya en uso.")
    register_form.password = hash_password(register_form.password)
    return user_repository.save(register_form.to_dict())



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ADMIN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#














































