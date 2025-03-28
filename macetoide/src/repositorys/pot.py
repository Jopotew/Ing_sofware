from typing import Optional

from macetoide.src.models.entities.log import Log
from macetoide.src.models.repository.repository import Repository
from macetoide.src.models.database.database import database as db


class PotRepository(Repository):
    def __init__(self):
        super().__init__()
        self.table = "pot"

    def get_all_logs(self, pot):
        logs_dict = db.get_all_logs_by_pot(pot.id)
        for log in logs_dict:
            if pot.id == log["id_pot"]:
                new = Log(
                    log["id"],
                    log["id_log"],
                    log["id_plant"],
                    log["temperature"],
                    log["soil_humidity"],
                    log["air_humidity"],
                    log["image_path"],
                    log["expert_advice"],
                )
                pot.add_log(new)
            else:
                print("Este log no pertenece al pot, Acceso cukatrap")
        return pot.logs

    def get_last_log(self, pot):
        last_log = None
        log = db.get_last_log_by_pot(pot.id)
        if pot.id == log["id"]:
            last_log = Log(
                log["id"],
                log["id_log"],
                log["id_plant"],
                log["temperature"],
                log["soil_humidity"],
                log["air_humidity"],
                log["image_path"],
                log["expert_advice"],
            )
        else:
            print("Este log no pertenece al pot, Acceso cukatrap")
        return last_log

    def set_last_checked(self, pot, new_time):
        return db.update_pot_last_checked(pot.id, new_time)

    def change_plant(self, pot, new_plant_id):
        return db.update_pot_id_plant(pot.id, new_plant_id)

    def change_analysis_time(self, pot, new_analysis_time):
        return db.update_pot_analysis_time(pot.id, new_analysis_time)


instance = PotRepository()
