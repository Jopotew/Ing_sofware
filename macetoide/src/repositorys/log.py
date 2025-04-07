from models.repository.repository import Repository
from models.entities.log import Log


class LogRepository(Repository):
    def __init__(self):
        super().__init__()
        self.table = "log"

    def get_logs(self, pot):

        log_list = self.db.get_all_logs(pot.id)

        for log in log_list:
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

    def get_last_log(self, pot): #controlar que se haya actualizado sino esta en pot agregarlo
        log_d = self.db.get_last_log(pot.id)
        if len(log_d) == 0:
            return None
        for log in pot.logs:
            if log_d["id"] == log.id:
                return log
        new_l = Log(log_d["id"],log_d["pot_id"], log_d["plant_id"],log_d["temperature"],log_d["soil_humidity"],log_d["air_humidity"],log_d["image_path"],log_d["expert_advice"])
        pot.logs.append(new_l)
        return new_l
    

    

instance = LogRepository()
