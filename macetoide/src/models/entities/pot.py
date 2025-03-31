from models.entities.log import Log
from models.entities.user import User
from models.entities.plant import Plant
from time import time


class Pot:
    """
    Class that represents a pot in the irrigation and control system.
    """

    def __init__(
        self,
        id: int,
        name: str,
        plant_id: int,
        analysis_time: time,
        user_id: int,
        last_checked: time
        


        
    ):
        """
        Initializes a new pot with data and related objects.
        """

        self.id = id
        self.name: str = name
        self.plant_id: int = plant_id
        self.analysis_time = analysis_time
        self.user_id: int = user_id
        self.last_checked = last_checked
        self.logs: list[Log] = []

    def set_last_checked(self):
        self.last_checked = time.now()

    def link_plant_id(self, new_plant_id):
        """
        Links a new plant object to the pot.
        """
        self.plant_id = new_plant_id

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
            "analysis_time": self.analysis_time,
            "plant_id": self.plant_id,
            "user_id": self.user.id,
            "last_checked": self.last_checked,
        }
