from typing import Optional


from macetoide.src.models.entities.pot import Pot
from macetoide.src.models.repository.repository import Repository
from macetoide.src.models.database.database import database as db


class PotRepository(Repository):
    def __init__(self):
        super().__init__()
        self.table = "pot"

    def get_pots(self, user_id: int) -> list[dict]:
        pots_dict = db.get_user_pots(user_id)
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
        return db.create_pot(pot)

    def save_pot(pot: Pot):
        return db.save_pot(pot)

    def set_last_checked(self, pot, new_time):
        return db.update_pot_last_checked(pot.id, new_time)

    def change_plant(self, pot, new_plant_id):
        return db.update_pot_id_plant(pot.id, new_plant_id)

    def change_analysis_time(self, pot, new_analysis_time):
        return db.update_pot_analysis_time(pot.id, new_analysis_time)


instance = PotRepository()
