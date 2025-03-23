from macetoide.src.models.entities.pot import Pot
from macetoide.src.models.entities.expert_advice import ExpertAdvice
from macetoide.src.models.entities.irrigation_status import StatusIrrigation
from macetoide.src.models.entities.pot_data import PotData
from macetoide.src.models.entities.analisis_time import AnalysisTime
from macetoide.src.models.entities.user import User
from macetoide.src.models.entities.irrigation_event import IrrigationEvent


class Log:
    """
    Class that represents a log record of a pot's analysis process.
    """

    def __init__(
        self,
        pot: Pot,
        pot_data: PotData,
        expert_advice: ExpertAdvice,
        irrigation_event: IrrigationEvent,
    ):
        """
        Initializes the log with all related objects and data.
        """
        self.id: int
        self.pot: Pot = pot
        self.pot_data: PotData = pot_data
        self.expert_advice: ExpertAdvice = expert_advice
        self.irrigation_event: IrrigationEvent = irrigation_event

    def generate_summary(self) -> str:
        """
        Generates a summary of the log with all relevant information.
        """
        irrigation_text = "Log completed"
        summary = (
            f"Pot: {self.pot.name}\n"
            f"Soil Humidity: {self.pot_data.soil_humidity}%\n"
            f"Air Humidity: {self.pot_data.air_humidity}"
            f"Temperature: {self.pot_data.temperature}°C\n"
            f"Image Path: {self.pot_data.image}\n"
            f"Irrigation Status: {irrigation_text}\n"
            f"Expert Advice: {self.expert_advice.detail}\n"
            f"User: {self.user.username}\n"
            f"Analysis Interval: {self.analysis_time.time}\n"
        )
        return summary
