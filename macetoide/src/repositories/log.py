from datetime import datetime
from random import uniform
from exceptions.exceptions import LogDataFetchError, DatabaseOperationError
from models.repository.repository import Repository
from repositories.pot import PotRepository, instance as pot_repository
from models.entities.log import Log
from models.entities.pot import Pot


class LogRepository(Repository):
    def __init__(self, pot_repository: PotRepository):
        super().__init__()
        self.pot_repository : PotRepository = pot_repository
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

    def get_last_log(self, pot: Pot) -> Log | dict:
        l = self.db.get_last_log(pot.id)

        if l is None:
            return {}

        return self.create_obj(l)

    def get_logs(self, pot: Pot, quantity: int = None) -> list[Log]:

        logs_data = self.db.get_all_logs(pot.id, limit=quantity)

        if not logs_data:
            raise LogDataFetchError("Failed to get logs from the database.")

        return [self.create_obj(log_data) for log_data in logs_data]

    


    def trigger_analysis(self, pot: Pot) -> bool:
        
        sensor_data = {
            "temperature": round(uniform(18.0, 30.0), 1),
            "soil_humidity": round(uniform(10.0, 70.0), 1),
            "air_humidity": round(uniform(30.0, 80.0), 1),
            "expert_advice": "Revisar humedad del suelo" if uniform(10.0, 70.0) < 30 else "Todo en orden"
        }

        new_log = {
            "pot_id": pot.id,
            "plant_id": pot.plant_id,
            "temperature": sensor_data["temperature"],
            "soil_humidity": sensor_data["soil_humidity"],
            "air_humidity": sensor_data["air_humidity"],
            "expert_advice": sensor_data["expert_advice"],
            "timestamp": datetime.now()
        }

        saved = self.db.save(new_log, self.table)
        if not saved:
            raise DatabaseOperationError("No se pudo guardar el log generado.")

        
        pot.set_last_checked(new_log["timestamp"])
        pot.update_modified()
        if not self.pot_repository.save(pot.get_dto()):
            raise DatabaseOperationError("No se pudo actualizar la maceta.")

        return True

instance = LogRepository(pot_repository)
