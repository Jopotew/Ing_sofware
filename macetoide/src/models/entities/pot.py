from macetoide.src.models.entities.log import Log
from macetoide.src.models.entities.user import User
from macetoide.src.models.entities.plant import Plant
from time import time


class Pot:
    """
    Class that represents a pot in the irrigation and control system.
    """

    def __init__(
        self,
        name: str,
        plant: Plant,
        analysis_time: int,
        user: User,
        


        
    ):
        """
        Initializes a new pot with data and related objects.
        """

        self.id = None
        self.name: str = name
        self.plant: Plant = plant
        self.analysis_time: int = analysis_time
        self.user: User = user
        self.last_checked: int = 1
        self.logs: list[Log] = []

    def set_last_checked(self):
        self.last_checked = time.now()

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


    def add_log(self, log: Log):
        self.logs.append(log)
        
    def get_last_log(self):
        return self.logs[-1]
    

    def get_dto(self):
        return {
            "id": self.id,
            "name": self.name,
            "plant": self.plant,
            "analysis_time": self.analysis_time,
            "user_id": self.user.id,
            "pot_data": self.pot_data,
            "last_checked": self.last_checked,
        }
