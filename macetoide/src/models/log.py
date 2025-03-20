from models.pot import Pot
from models.expert_advice import ExpertAdvice
from models.irrigation_status import StatusIrrigation
from models.data_pot import DataPot
from models.analisis_time import AnalysisTime
from models.user import User
from models.irrigation_event import IrrigationEvent


class Log:
    """
    Class that represents a log record of a pot's analysis process.
    """

    def __init__(self, pot: Pot, data_pot: DataPot, expert_advice: ExpertAdvice, irrigation_event: IrrigationEvent):
        """
        Initializes the log with all related objects and data.
        """
        self.pot:Pot = pot.user
        self.user: User = pot.user   
        self.data_pot: DataPot = data_pot                  
        self.analysis_time: AnalysisTime = pot.analysis_time          
        self.expert_advice: ExpertAdvice = expert_advice  
        self.irrigation_event: IrrigationEvent = irrigation_event     




    def generate_summary(self) -> str:
        """
        Generates a summary of the log with all relevant information.
        """
        irrigation_text = "Irrigation completed" if self.irrigation_status.status else "No irrigation"
        summary = (
            f"Pot: {self.pot.name}\n"
            f"Humidity: {self.data_pot.humidity}%\n"
            f"Temperature: {self.data_pot.temperature}°C\n"
            f"Image Path: {self.data_pot.image}\n"
            f"Irrigation Status: {irrigation_text}\n"
            f"Expert Advice: {self.expert_advice.detail}\n"
            f"User: {self.user.username}\n"
            f"Analysis Interval: {self.analysis_time.time}\n"
        )
        return summary
