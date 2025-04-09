from models.repository.repository import Repository
from models.entities.log import Log
from models.entities.pot import Pot


class LogRepository(Repository):
    def __init__(self):
        super().__init__()
        self.table = "log"

    def create_obj(self, data: dict) -> Log:
        log = Log(
            data["id"],
            data["pot_id"],
            data["plant_id"],
            data["temperature"],
            data["soild_humidity"],
            data["air_humidity"],
            data["image_path"],
            data["expert_advice"],
        )
        return log

    def last_log(self, pot: Pot) -> Log | dict:

        l = self.db.get_last_log(pot.id)

        if l == None:
            return {}

        log = self.create_obj(l)
        return log

    def get_logs(self, pot: Pot, quantity: int = None) -> list | dict:

        ls = self.db.get_all_logs(pot.id, limit=quantity)

        if not ls:
            return {
                "function": "get_logs",
                "status": False,
                "detail": "Failed to get logs in database.",
            }

        return [self.create_obj(log_data) for log_data in ls]


instance = LogRepository()
