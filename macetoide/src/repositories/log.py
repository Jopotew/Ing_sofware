from models.repository.repository import Repository
from models.entities.log import Log
from models.entities.pot import Pot


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
    

    def get_pot_logs(self, pot: Pot, quantity: int = None):
        logs = self.db.get_all_logs(pot.id)
        if quantity is None:
            return logs
        else:
            return logs[-quantity:] 
        
        
    def get_last_log(self, pot: Pot) -> Log: 
        log_d = self.db.get_last_log(pot.id)
        if log_d is None:
            return None
        log = self.create_obj(log_d)
        return log
    

    

instance = LogRepository()
