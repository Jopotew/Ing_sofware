from dataclasses import dataclass
from datetime import datetime
from models.entities.plant import Plant


@dataclass
class Log:
    def __init__(
        self,
        id: int,
        pot_id: int,
        plant_id: int,
        temperature: float,
        soil_humidity: float,
        air_humidity: float,
        expert_advice: str,
    ):

        self.id = (id,)
        self.pot_id: int = pot_id
        self.plant_id: int = plant_id
        self.temperature: float = temperature
        self.soil_humidity: float = soil_humidity
        self.air_humidity: float = air_humidity
        self.expert_advice: str = expert_advice
        self.timestamp: datetime = datetime.now()
