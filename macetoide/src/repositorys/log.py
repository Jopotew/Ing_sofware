from models.repository.repository import Repository
from models.entities.log import Log
from models.database.database import database as db

class LogRepository(Repository):
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


instance = LogRepository()
