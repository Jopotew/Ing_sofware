from exceptions.exceptions import LogDataFetchError, DatabaseOperationError
from models.repository.repository import Repository
from models.entities.log import Log
from models.entities.pot import Pot


class LogRepository(Repository):
    def __init__(self):
        super().__init__()
        self.table = "log"

    def create_obj(self, data: dict) -> Log:
        return Log(
            data["id"],
            data["pot_id"],
            data["plant_id"],
            data["temperature"],
            data["soild_humidity"],
            data["air_humidity"],
            data["image_path"],
            data["expert_advice"],
        )

    def last_log(self, pot: Pot) -> Log | dict:
        l = self.db.get_last_log(pot.id)

        if l is None:
            return {}

        return self.create_obj(l)

    def get_logs(self, pot: Pot, quantity: int = None) -> list[Log]:

        logs_data = self.db.get_all_logs(pot.id, limit=quantity)

        if not logs_data:
            raise LogDataFetchError("Failed to get logs from the database.")

        return [self.create_obj(log_data) for log_data in logs_data]


instance = LogRepository()
