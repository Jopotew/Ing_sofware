from models.entities.log import Log
from models.entities.user import User
from models.entities.plant import Plant
from datetime import datetime


class Pot:
    """
    Class that represents a pot in the irrigation and control system.
    """

    def __init__(
        self,
        id: int,
        name: str,
        plant_id: int,
        analysis_time: datetime,
        user_id: int,
        last_checked: datetime,
        last_modified: int
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
        self.last_modified: int = last_modified
        self.logs: list[Log] = []

    def set_last_checked(self):
        self.last_checked = datetime.now()

    def link_plant_id(self, new_plant_id):
        self.plant_id = new_plant_id

    def link_analysis_time(self, new_time):
        self.analysis_time = new_time

    def update_modified(self):
        self.last_modified = datetime.now()   

    def add_log(self, log: Log):
        self.logs.append(log)
        
    def get_last_log(self):
        return self.logs[-1]
    

    def get_dto(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "analysis_time": self.analysis_time,
            "plant_id": self.plant_id,
            "user_id": self.user_id,
            "last_checked": self.last_checked,
            "last_modified": self.last_modified
        }
