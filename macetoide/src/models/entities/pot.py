
from macetoide.src.models.entities.entity import Entity
from macetoide.src.models.entities.analisis_time import AnalysisTime
from macetoide.src.models.entities.user import User
from macetoide.src.models.entities.plant import Plant
from datetime import datetime


class Pot(Entity):
    """
    Class that represents a pot in the irrigation and control system.
    """

    def __init__(
        self, id: int, name: str, plant: Plant, analysis_time: AnalysisTime, user: User
    ):
        """
        Initializes a new pot with data and related objects.
        """
        self.name: str = name
        self.plant: Plant = plant
        self.analysis_time: AnalysisTime = analysis_time
        self.user: User = user
        self.id: int = id
        self.last_checked: str

    def last_checked(self):
        self.last_checked = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def link_plant(self, new_plant):
        """
        Links a new plant object to the pot.
        """
        self.plant = new_plant

    def link_analysis_time(self, new_time):
        """
        Links a new analysis time object to the pot.
        """
        self.analysis_time = new_time
