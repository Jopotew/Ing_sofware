from macetoide.src.models.entities.analisis_time import AnalysisTime
from macetoide.src.models.entities.expert_advice import ExpertAdvice
from macetoide.src.models.entities.irrigation_event import IrrigationEvent
from macetoide.src.models.entities.log import Log
from macetoide.src.models.entities.plant import Plant
from macetoide.src.models.entities.pot import Pot
from macetoide.src.models.entities.pot_data import PotData
from macetoide.src.models.entities.user import User


class LogRepository:
    """
    Class responsible for retrieving Log entries from the database
    and rebuilding the full Log object.
    """

    def __init__(self, db_connection):
        self.db = db_connection

    def get_log_by_id(self, log_id: int) -> Log:
        """
        Retrieves a log entry from the database and reconstructs the Log object.

        Args:
            log_id (int): The unique identifier of the log entry.

        Returns:
            Log: The reconstructed Log object.
        """

        log_data = self.db.fetch_log_data(log_id)

        pot = Pot(
            name=log_data["pot_name"],
            plant=Plant(log_data["plant_name"], log_data["plant_species"]),
            analysis_time=AnalysisTime(
                log_data["analysis_minutes"], log_data["analysis_hours"]
            ),
            user=User(
                log_data["user_name"],
                log_data["user_surname"],
                log_data["username"],
                log_data["mail"],
                "*****",
            ),
        )

        pot_data = PotData(
            soil_humidity=log_data["soil_humidity"],
            air_humidity=log_data["air_humidity"],
            temperature=log_data["temperature"],
            image=log_data["image_path"],
        )

        expert_advice = ExpertAdvice()
        expert_advice.detail = log_data["expert_detail"]

        irrigation_event = IrrigationEvent(
            time_active=log_data["irrigation_duration"], watered=log_data["watered"]
        )

        reconstructed_log = Log(
            pot=pot,
            pot_data=pot_data,
            expert_advice=expert_advice,
            irrigation_event=irrigation_event,
        )

        return reconstructed_log
