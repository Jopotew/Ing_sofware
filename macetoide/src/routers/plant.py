from fastapi import APIRouter, Depends
from typing import Annotated
from models.entities.viewer_user import ViewerUser
from routers.auth import get_current_user
from repositories.plant import instance as plant_repository
from models.forms.base_models import PlantForm

router = APIRouter(tags=["Plants"])


@router.get("/plants")
def get_all_plants(user: Annotated[ViewerUser, Depends(get_current_user)]):
    return plant_repository.get_all()


@router.get("/user/pots/pot/plant")
def get_plant_by_id(
    plant: PlantForm, user: Annotated[ViewerUser, Depends(get_current_user)]
):
    return plant_repository.get_by_id(plant_repository.create_obj(plant.to_dict()).id)


@router.get("/plants/user")
def get_user_plants(user: Annotated[ViewerUser, Depends(get_current_user)]):
    return plant_repository.get_plants_by_user(user)



#get species
#get description