from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from models.entities.pot import Pot
from models.entities.plant import Plant
from models.entities.viewer_user import ViewerUser
from routers.auth import get_current_user
from repositories.log import instance as log_repository
from repositories.pot import instance as pot_repository
from repositories.plant import instance as plant_repository
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


@router.get("/pot/status")
def get_pot_status(
    pot: PotForm, user: Annotated[ViewerUser, Depends(get_current_user)]
):
    pot_obj: Pot = pot_repository.create_obj(pot.to_dict())

    if pot_obj.user_id != user.id:
        raise HTTPException(status_code=403, detail="No autorizado")

    log = log_repository.get_last_log(pot_obj)

    if not log:
        return {"status": "No hay registros para esta maceta."}

    plant: Plant = plant_repository.get_by_id(log.plant_id)

    estado_riego = "Humedad adecuada" if log.soil_humidity >= 30 else "Necesita riego"

    return {
        "temperatura": log.temperature,
        "humedad_suelo": log.soil_humidity,
        "humedad_aire": log.air_humidity,
        "estado_riego": estado_riego,
        "timestamp": log.timestamp.strftime("%m-%d %H:%M:%S"),
        "descripcion": log.expert_advice,
        "planta": {
            "nombre": plant.name,
            "especie": plant.species,
            "descripcion": plant.description,
        },
    }


@router.get("/pot/history")
def get_pot_log_history(
    pot: PotForm, user: Annotated[ViewerUser, Depends(get_current_user)]
):
    pot_obj: Pot = pot_repository.create_obj(pot.to_dict())

    if pot_obj.user_id != user.id:
        raise HTTPException(status_code=403, detail="No autorizado")

    logs = log_repository.get_logs(pot_obj)

    sorted_logs = sorted(logs, key=lambda l: l.timestamp, reverse=True)

    return [log.get_dto() for log in sorted_logs]
