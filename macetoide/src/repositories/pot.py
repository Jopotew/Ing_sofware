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
        self.table = "pot"

    def create_objs(self, data: dict) -> Pot:
        return Pot(
            data["id"],
            data["name"],
            data["id_plant"],
            data["analysis_time"],
            data["id_user"],
            data["last_checked"],
        )

    def get_user_pots(self, user: User) -> list[Pot]:
        p = self.db.get_user_pots(user.id)

        if p is None:
            raise DatabaseOperationError("Failed to fetch pots from database.")

        if len(p) == 0:
            return []
        
        for i in p:
            user.add_pot(self.create_obj(i))

        return user.pots

    def set_last_checked(self, pot: Pot, new_time) -> bool:
        pot.set_last_checked(new_time)
        pot.update_modified()
        if not self.db.save(pot.get_dto):
            raise DatabaseOperationError("Failed to update pot's last_checked in database.")
        return True

    def change_plant(self, pot: Pot, new_plant_id) -> bool:
        pot.link_plant_id(new_plant_id)
        pot.update_modified()
        if not self.db.save(pot.get_dto):
            raise DatabaseOperationError("Failed to update pot's plant_id in database.")
        return True

    def change_analysis_time(self, pot: Pot, new_analysis_time) -> bool:
        pot.link_analysis_time(new_analysis_time)
        pot.update_modified()
        if not self.db.save(pot.get_dto):
            raise DatabaseOperationError("Failed to update pot's analysis_time in database.")
        return True



instance = PotRepository()
