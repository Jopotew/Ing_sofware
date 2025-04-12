from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from macetoide.src.models.entities.pot import Pot
from models.entities.user import User
from routers.auth import get_current_user
from repositories.pot import instance as pot_repository
from models.forms.base_models import PotForm

router = APIRouter(prefix="/user/pots", tags=["Pot"])


@router.get("/")
def get_user_pots(user: Annotated[User, Depends(get_current_user)]):
    return pot_repository.get_user_pots(user)


@router.post("/pot")
def create_pot(pot: PotForm, user: Annotated[User, Depends(get_current_user)]):
    pot_obj: Pot = pot_repository.create_obj(pot.to_dict())
    if pot_obj.user_id != user.id:
        raise HTTPException(status_code=403, detail="No autorizado")
    return pot_repository.save(pot.to_dict())



@router.post("/")
def save_pot(pot: PotForm, user: Annotated[User, Depends(get_current_user)]):
    pot_obj: Pot = pot_repository.create_obj(pot.to_dict())
    if pot_obj.user_id != user.id:
        raise HTTPException(status_code=403, detail="No autorizado")
    return pot_repository.save(pot.to_dict())


@router.get("/pot")
def get_pot_by_id(pot: PotForm, user: Annotated[User, Depends(get_current_user)]):
    pot_obj: Pot = pot_repository.create_obj(pot.to_dict())
    if pot_obj.user_id != user.id:
        raise HTTPException(status_code=403, detail="No autorizado")
    return pot_repository.get_by_id(pot_obj.id)


@router.post("/pot/update")
def update_pot(pot: PotForm, user: Annotated[User, Depends(get_current_user)]):
    pot_obj: Pot = pot_repository.create_obj(pot.to_dict())
    if pot_obj.user_id != user.id:
        raise HTTPException(status_code=403, detail="No autorizado")
    return pot_repository.save(pot.to_dict())


@router.post("/pot/delete")
def delete_pot(pot: PotForm, user: Annotated[User, Depends(get_current_user)]):
    pot_obj: Pot = pot_repository.create_obj(pot.to_dict())
    if pot_obj.user_id != user.id:
        raise HTTPException(status_code=403, detail="No autorizado")
    return pot_repository.delete(pot.id)
