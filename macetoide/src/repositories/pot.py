from datetime import datetime
import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "..")
sys.path.append(src_path)

from exceptions.exceptions import (
    DatabaseOperationError,
    PotNotFoundError,
)
from models.entities.user import User
from models.entities.pot import Pot
from models.repository.repository import Repository
from typing import Optional


class PotRepository(Repository):
    def __init__(self):
        super().__init__()
        self.table = "pots"

    def create_obj(self, data: dict) -> Pot:
     
        analysis_time = float(data["analysis_time"])
        
        last_checked = data.get("last_checked")
        if isinstance(last_checked, str):
            last_checked = datetime.strptime(last_checked, "%Y-%m-%d %H:%M:%S")

        return Pot(
            data["id"],
            data["name"],
            data["plant_id"],
            analysis_time,
            data["user_id"],
            last_checked,
        )
    
    def get_user_pots(self, user_id: int) -> list[Pot]:
        p = self.db.get_user_pots(user_id)
        p_list: list[Pot] = []

        if p is None:
            raise DatabaseOperationError("Failed to fetch pots from database.")

        if len(p) == 0:
            return []

        for i in p:
            p_list.add_pot(self.create_obj(i))

        return p_list

    def set_last_checked(self, pot: Pot, new_time) -> dict:
        pot.set_last_checked(new_time)
        pot.update_modified()

        if not self.db.save(pot.get_dto()):
            raise DatabaseOperationError(
                "Failed to update pot's last_checked in database."
            )

        return {"message": f"Última revisión actualizada para la maceta {pot.id}."}

    def change_plant(self, pot: Pot, new_plant_id: int) -> dict:
        pot.link_plant_id(new_plant_id)
        pot.update_modified()

        if not self.db.save(pot.get_dto()):
            raise DatabaseOperationError("Failed to update pot's plant_id in database.")

        return {
            "message": f"Planta {new_plant_id} asignada correctamente a la maceta {pot.id}."
        }

    def change_analysis_time(self, pot: Pot, new_analysis_time) -> dict:
        pot.link_analysis_time(new_analysis_time)
        pot.update_modified()

        if not self.db.save(pot.get_dto()):
            raise DatabaseOperationError(
                "Failed to update pot's analysis_time in database."
            )

        return {"message": f"Hora de análisis actualizada para la maceta {pot.id}."}

    def change_name(self, pot: Pot, new_name: str) -> bool:
        pot.name = new_name
        pot.update_modified()

        success = self.db.update_pot_name(pot.id, new_name)

        if not success:
            raise DatabaseOperationError(
                "No se pudo actualizar el nombre de la maceta."
            )

        return {
            "message": f"Nombre de la maceta {pot.id} actualizado a '{new_name}' correctamente."
        }


instance = PotRepository()
