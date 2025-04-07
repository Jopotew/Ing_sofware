import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "..")
sys.path.append(src_path)


from typing import Optional


from models.entities.pot import Pot
from models.repository.repository import Repository



class PotRepository(Repository):
    def __init__(self):
        super().__init__()
        self.table = "pot"


    def create_pot(dict: dict):
        pot = Pot(dict["id"], dict["name"], dict["id_plant"], dict["analysis_time"], dict["id_user"], dict["last_checked"] )
        return pot


    def get_pots(self, user_id: int) -> list[dict]:
        pots_dict = self.db.get_user_pots(user_id)
        user_pots: list[dict] = []

        for pot in pots_dict:
            if pot["id_user"] == user_id:
                new = Pot(
                    pot["id"],
                    pot["name"],
                    pot["id_plant"],
                    pot["analysis_time"],
                    pot["user"],
                    pot["last_checked"],
                )
                user_pots.append(new.get_dto())
        return user_pots

    def new_pot(pot: Pot):
        return self.db.create_pot(pot)

    def save_pot(pot: dict):
        return self.db.save(pot)

    def set_last_checked(self, pot, new_time):
        return self.db.update_pot_last_checked(pot.id, new_time)

    def change_plant(self, pot, new_plant_id):
        return self.db.update_pot_id_plant(pot.id, new_plant_id)

    def change_analysis_time(self, pot, new_analysis_time):
        return self.db.update_pot_analysis_time(pot.id, new_analysis_time)


instance = PotRepository()
    