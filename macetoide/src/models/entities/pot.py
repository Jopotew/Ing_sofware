from macetoide.src.models.entities.analisis_time import AnalysisTime
from models.entities.user import User
from models.entities.plant import Plant
from datetime import datetime 



class Pot:
    """
    Class that represents a pot in the irrigation and control system.
    """

    def __init__(self, name: str, plant, analysis_time, user):
        """
        Initializes a new pot with data and related objects.
        """
        self.name = name
        self.plant: Plant = plant                  
        self.analysis_time: AnalysisTime = analysis_time  
        self.user: User = user
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

    