from fastapi import APIRouter, HTTPException, Depends, status
from typing import Annotated
from models.forms.base_models import AdminRegisterForm, DataUpdateForm, RegisterForm
from models.entities.viewer_user import ViewerUser
from models.entities.admin_user import AdminUser
from repositories.user import instance as user_repository
from repositories.pot import instance as pot_repository
from repositories.log import instance as log_repository
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




@router.get("/admin/user/{username}")
def get_user_by_username(
    username: str,
    user: Annotated[AdminUser, Depends(get_current_user)]
):
    if not isinstance(user, AdminUser):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado")

    target_user = user_repository.get_by_username(username)

    if isinstance(target_user, ViewerUser):
        return target_user.get_dto()

    return target_user.get_dto()


@router.get("/admin/users")
def get_all_users(user: Annotated[AdminUser, Depends(get_current_user)]):
    if not isinstance(user, AdminUser):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado")

    users = user_repository.get_all()
    return [u.get_dto() for u in users]


@router.get("/profile")
def get_profile(user: Annotated[ViewerUser | AdminUser, Depends(get_current_user)]):
    return user.get_dto()


@router.get("/admin/user/{username}/pots")
def get_user_pots_by_username(
    username: str,
    user: Annotated[AdminUser, Depends(get_current_user)]
):
    if not isinstance(user, AdminUser):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado")

    target_user = user_repository.get_by_username(username)
    return [p.get_dto() for p in target_user.pots]


@router.get("/admin/pots/count")
def get_total_pot_count(user: Annotated[AdminUser, Depends(get_current_user)]):
    if not isinstance(user, AdminUser):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado")

    pots = pot_repository.get_all()
    return {"total_pots": len(pots)}


@router.get("/admin/logs")
def get_all_logs(user: Annotated[AdminUser, Depends(get_current_user)]):
    if not isinstance(user, AdminUser):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado")

    logs = log_repository.get_all()
    return [log.get_dto() for log in logs]


@router.post("/admin/user/create")
def create_user_by_admin(
    user: Annotated[AdminUser, Depends(get_current_user)],
    new_user: AdminRegisterForm
):
    if not isinstance(user, AdminUser):
        raise HTTPException(status_code=403, detail="No autorizado")

    if user_repository.validate_user(new_user.username):
        raise HTTPException(status_code=409, detail="El nombre de usuario ya existe.")

    user_data = new_user.to_dict()
    user_data["password"] = hash_password(user_data["password"])

    user_repository.save(user_data)

    return {
        "message": f"Usuario '{new_user.username}' creado como {'admin' if new_user.admin_role else 'viewer'}."
    }


@router.delete("/admin/user/{username}")
def delete_user_by_username(
    username: str,
    user: Annotated[AdminUser, Depends(get_current_user)]
):
    if not isinstance(user, AdminUser):
        raise HTTPException(status_code=403, detail="No autorizado")

    user_repository.delete_by_username(username)
    return {"message": f"Usuario '{username}' eliminado correctamente."}



@router.get("/admin/analytics")
def get_analytics(user: Annotated[AdminUser, Depends(get_current_user)]):
    if not isinstance(user, AdminUser):
        raise HTTPException(status_code=403, detail="No autorizado")

    return user_repository.get_system_stats()

































