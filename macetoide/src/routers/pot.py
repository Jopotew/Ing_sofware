from fastapi import APIRouter, Body, HTTPException, Depends
from typing import Annotated
from models.entities.pot import Pot
from models.entities.viewer_user import ViewerUser
from routers.auth import get_current_user
from repositories.pot import instance as pot_repository
from models.forms.base_models import PotForm

router = APIRouter(prefix="/user/pots", tags=["Pot"])


@router.get("/")
def get_user_pots(user: Annotated[ViewerUser, Depends(get_current_user)]):
    return pot_repository.get_user_pots(user)


@router.post("/pot")
def create_pot(pot: PotForm, user: Annotated[ViewerUser, Depends(get_current_user)]):
    pot_obj: Pot = pot_repository.create_obj(pot.to_dict())
    if pot_obj.user_id != user.id:
        raise HTTPException(status_code=403, detail="No autorizado")
    return pot_repository.save(pot.to_dict())


@router.post("/")
def save_pot(pot: PotForm, user: Annotated[ViewerUser, Depends(get_current_user)]):
    pot_obj: Pot = pot_repository.create_obj(pot.to_dict())
    if pot_obj.user_id != user.id:
        raise HTTPException(status_code=403, detail="No autorizado")
    return pot_repository.save(pot.to_dict())


@router.get("/pot")
def get_pot_by_id(pot: PotForm, user: Annotated[ViewerUser, Depends(get_current_user)]):
    pot_obj: Pot = pot_repository.create_obj(pot.to_dict())
    if pot_obj.user_id != user.id:
        raise HTTPException(status_code=403, detail="No autorizado")
    return pot_repository.get_by_id(pot_obj.id)


@router.post("/pot/update")
def update_pot(pot: PotForm, user: Annotated[ViewerUser, Depends(get_current_user)]):
    pot_obj: Pot = pot_repository.create_obj(pot.to_dict())
    if pot_obj.user_id != user.id:
        raise HTTPException(status_code=403, detail="No autorizado")
    return pot_repository.save(pot.to_dict())


@router.post("/pot/delete")
def delete_pot(pot: PotForm, user: Annotated[ViewerUser, Depends(get_current_user)]):
    pot_obj: Pot = pot_repository.create_obj(pot.to_dict())
    if pot_obj.user_id != user.id:
        raise HTTPException(status_code=403, detail="No autorizado")
    return pot_repository.delete(pot.id)


@router.post("/pot/update/name")
def update_pot_name(
    user: Annotated[ViewerUser, Depends(get_current_user)],
    pot: PotForm,
    new_name: str = Body(...),
):
    pot_obj: Pot = pot_repository.create_obj(pot.to_dict())

    if pot_obj.user_id != user.id:
        raise HTTPException(status_code=403, detail="No autorizado")

    return pot_repository.change_name(pot_obj, new_name)


@router.post("/pot/assign")
def assign_plant_to_pot(
    user: Annotated[ViewerUser, Depends(get_current_user)],
    pot: PotForm,
    new_plant_id: int = Body(...),
):
    pot_obj: Pot = pot_repository.create_obj(pot.to_dict())

    if pot_obj.user_id != user.id:
        raise HTTPException(status_code=403, detail="No autorizado")

    return pot_repository.change_plant(pot_obj, new_plant_id)
