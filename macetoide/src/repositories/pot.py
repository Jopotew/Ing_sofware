import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "..")
sys.path.append(src_path)


from typing import Optional

from models.entities.user import User
from models.entities.pot import Pot
from models.repository.repository import Repository



class PotRepository(Repository):
    def __init__(self):
        super().__init__()
        self.table = "pot"

    def create_objs(self, data: dict) -> Pot:
        pot = Pot(
            data["id"],
            data["name"],
            data["id_plant"],
            data["analysis_time"],
            data["id_user"],
            data["last_checked"] 
            )
        
        return pot
        
    def get_user_pots(self, user: User) -> Optional[list]:
        p = self.db.get_user_pots(user.id)

        if not p:
            return {"function":"get_user_pots", "status": False, "detail": "Failed to get data from database"}
        
        if len(p) == 0:
            return []
        
        for i in p:
            user.add_pot(self.create_obj(i))

        return user.pots

    def set_last_checked(self, pot: Pot, new_time):
        pot.set_last_checked(new_time)
        pot.update_modified()
        if self.db.save(pot.get_dto):
            return True
        else:
            return {}

    def change_plant(self, pot: Pot, new_plant_id):
        pot.link_plant_id(new_plant_id)
        pot.update_modified()
        if self.db.save(pot.get_dto):
            return True
        else:
            return {}

    def change_analysis_time(self, pot: Pot, new_analysis_time):
        pot.link_analysis_time(new_analysis_time)
        pot.update_modified()
        if self.db.save(pot.get_dto):
            return True
        else:
            return {}
    


instance = PotRepository()
    