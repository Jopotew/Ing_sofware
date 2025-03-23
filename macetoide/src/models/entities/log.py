from dataclasses import dataclass
from time import time
from macetoide.src.models.entities.plant import Plant
from macetoide.src.models.entities.pot_data import PotData


@dataclass
class Log:
    """
    Class that represents a log record of a pot's analysis process & status.
    """

    def __init__(self, pot_id: int, plant: Plant, pot_data: PotData):
        """
        Initializes the log with all related objects and data.
        """
        self.pot_id: int = pot_id
        self.plant: Plant = plant
        self.pot_data: PotData = pot_data
        self.timestamp: float = time.now()
