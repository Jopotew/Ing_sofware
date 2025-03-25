from dataclasses import dataclass
from time import time
from macetoide.src.models.entities.plant import Plant
from macetoide.src.models.entities.pot_data import PotData


@dataclass
class Log:
    """
    Class that represents a log record of a pot's analysis process & status.
    """

    def __init__(
            self, pot_id: int,
            plant: Plant, 
            temperature: float, 
            soil_humidity:float, 
            air_humidity: float, 
            image_path: str, 
            expert_advice: str 
            ):
        
        """
        Initializes the log with all related objects and data.
        """
        self.pot_id: int = pot_id
        self.plant: Plant = plant
        self.temperature: float = temperature
        self.soil_humidity: float = soil_humidity
        self.air_humidity: float = air_humidity
        self.image_path: str = image_path
        self.expert_advice: str = expert_advice
        self.timestamp: float = time.now()
