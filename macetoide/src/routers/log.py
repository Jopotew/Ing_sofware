from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from models.entities.pot import Pot
from models.entities.viewer_user import ViewerUser
from routers.auth import get_current_user
from repositories.log import instance as log_repository
from repositories.pot import instance as pot_repository
from models.forms.base_models import LogForm, PotForm

router = APIRouter(prefix="/user/pots/pot/logs", tags=["Log"])


@router.get("/log")
def get_last_log(pot: PotForm, user: Annotated[ViewerUser, Depends(get_current_user)]):
    pot_obj: Pot = pot_repository.create_obj(pot.to_dict())
    if pot_obj.user_id != user.id:
        raise HTTPException(status_code=403, detail="No autorizado")
    return log_repository.get_last_log(pot_obj)


@router.get("/")
def get_logs(pot: PotForm, user: Annotated[ViewerUser, Depends(get_current_user)]):
    pot_obj: Pot = pot_repository.create_obj(pot.to_dict())
    if pot_obj.user_id != user.id:
        raise HTTPException(status_code=403, detail="No autorizado")
    return log_repository.get_logs(pot_obj)


@router.post("/log")
def save_log(log: LogForm, user: Annotated[ViewerUser, Depends(get_current_user)]):
    if log.pot_id != user.id:
        raise HTTPException(status_code=403, detail="No autorizado")
    return log_repository.save(log.to_dict())


@router.get("/all")
def get_all_logs(pot: PotForm, user: Annotated[ViewerUser, Depends(get_current_user)]):

    pot_obj: Pot = pot_repository.create_obj(pot.to_dict())
    if pot_obj.user_id != user.id:
        raise HTTPException(status_code=403, detail="No autorizado")
    return log_repository.get_logs(pot_obj)


@router.get("/last10")
def get_last_10_logs(
    pot: PotForm, user: Annotated[ViewerUser, Depends(get_current_user)]
):
    pot_obj: Pot = pot_repository.create_obj(pot.to_dict())
    if pot_obj.user_id != user.id:
        raise HTTPException(status_code=403, detail="No autorizado")
    return log_repository.get_logs(pot_obj, quantity=10)
