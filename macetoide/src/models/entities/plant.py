from models.entities.open_ai_api import Chatbot
from datetime import datetime


class Plant:
    """
    Class that represents a plant in the pot system.
    """

    def __init__(self, name: str, last_modified, species: str = None, description: str = None):
        """
        Initializes a new plant with its name, species, and an optional description.
        """
        self.id: int = None
        self.name: str = name
        self.species: str = species
        self.description: str = description
        self.last_modified = last_modified

    def update_modified(self):
        self.last_modified = datetime.now()       

    def get_dto(self):
        return {
            "id": self.id,
            "name": self.name,
            "species": self.species,
            "description": self.description,
            "last_modified": self.last_modified
        }