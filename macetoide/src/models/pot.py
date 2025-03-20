from models.analisis_time import AnalysisTime
from models.user import User
from models.plant import Plant



class Pot:
    """
    Class that represents a pot in the irrigation and control system.
    """

    def __init__(self, name: str, plant, analysis_time, user):
        """
        Initializes a new pot with data and related objects.
        """
        self.name = name
        self.plant: Plant = plant                  # Plant object
        self.analysis_time: AnalysisTime = analysis_time  # AnalysisTime object
        self.user: User = user

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

    