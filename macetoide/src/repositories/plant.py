from typing import Optional
from models.repository.repository import Repository
from models.entities.plant import Plant
from models.entities.open_ai_api import Chatbot, instance_chatbot as chatbot


class PlantRepository(Repository):
    def __init__(self, chatbot):
        super().__init__()
        self.table = "plant"
        self.chatbot: Chatbot = chatbot

    def create_obj(self, data: dict) -> Plant:
        plant = Plant(
            data["name"], data["last_modified"], data["species"], data["description"]
        )
        self._manage_info(plant)
        return plant

    def _manage_info(self, plant: Plant) -> Optional[dict]:
        updated = False

        if not plant.description:
            plant.description = self.chatbot.ask_description(plant.name)
            updated = True

        if not plant.species:
            plant.species = self.chatbot.ask_species(plant.name)
            updated = True

        if updated:
            plant.update_modified()
            st = self.save(plant.get_dto)
            if st:
                return st
            return {
                "Function": "Manage_info()",
                "status": False,
                "detail": "Error while saving in BD",
            }
        return


instance = PlantRepository(chatbot)
