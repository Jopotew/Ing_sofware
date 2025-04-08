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

    def create_objs(data: dict) -> Pot:
        pot = Pot(data["id"], data["name"], data["id_plant"], data["analysis_time"], data["id_user"], data["last_checked"] )
        return pot
        
    def get_user_pots(self, user_id) -> list:
        pots: list = []
        p_dict = self.db.get_user_pots(user_id)
        for i in p_dict:
            pots.append(self.create_obj(i))
        return pots

    def new_pot(self, pot: Pot):
        return self.db.create_pot(pot)

    def save_pot(self, pot: dict):
        return self.db.save(pot)

    def set_last_checked(self, pot, new_time):
        return self.db.update_pot_last_checked(pot.id, new_time)

    def change_plant(self, pot, new_plant_id):
        return self.db.update_pot_id_plant(pot.id, new_plant_id)

    def change_analysis_time(self, pot, new_analysis_time):
        return self.db.update_pot_analysis_time(pot.id, new_analysis_time)
    
    def update_timestamp_modifier(self):
        pass


instance = PotRepository()
    