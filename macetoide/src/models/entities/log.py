from dataclasses import dataclass
from datetime import datetime
from models.entities.plant import Plant


@dataclass
class Log:
    """
    Class that represents a log record of a pot's analysis process & status.
    """

    def __init__(
        self,
        id: int,
        pot_id: int,
        plant_id: int,
        temperature: float,
        soil_humidity: float,
        air_humidity: float,
        image_path: str,
        expert_advice: str,
    ):

        self.id = (id,)
        self.pot_id: int = pot_id
        self.plant_id: int = plant_id
        self.temperature: float = temperature
        self.soil_humidity: float = soil_humidity
        self.air_humidity: float = air_humidity
        self.image_path: str = image_path
        self.expert_advice: str = expert_advice
        self.timestamp: datetime = datetime.now()
