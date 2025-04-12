from fastapi import APIRouter, Depends
from typing import Annotated
from models.entities.user import User
from routers.auth import get_current_user
from repositories.plant import instance as plant_repository
from models.forms.base_models import PlantForm

router = APIRouter(tags=["Plants"])


@router.get("/plants")
def get_all_plants(user: Annotated[User, Depends(get_current_user)]):
    return plant_repository.get_all()


@router.get("/user/pots/pot/plant")
def get_plant_by_id(plant: PlantForm, user: Annotated[User, Depends(get_current_user)]):
    return plant_repository.get_by_id(plant_repository.create_obj(plant.to_dict()).id)
