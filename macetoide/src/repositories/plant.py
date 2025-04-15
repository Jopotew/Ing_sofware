from exceptions.exceptions import PlantSearchError, DatabaseOperationError
from models.entities.viewer_user import ViewerUser
from models.repository.repository import Repository
from models.entities.plant import Plant

# from models.entities.open_ai_api import Chatbot, instance_chatbot as chatbot


class PlantRepository(Repository):
    def __init__(self, chatbot: str):
        super().__init__()
        self.table = "plant"
        self.chatbot = chatbot

    def create_obj(self, data: dict) -> Plant:
        plant = Plant(
            data["name"], data["last_modified"], data["species"], data["description"]
        )
        self._manage_info(plant)
        return plant

    def get_list_plants_in(self, p_dict: dict) -> list:
        if not p_dict:
            raise ValueError("Input dictionary is empty.")

        p_raw_list: list[dict] = []
        p_obj_list: list[Plant] = []

        for entry in p_dict.values():
            p = self.db.get_by_name(entry["name"], self.table)

            if p is None:
                raise PlantSearchError(f"Plant '{entry['name']}' does not exist.")

            if not p:
                raise DatabaseOperationError("Error while doing database operation.")

            p_raw_list.append(p)

        for data in p_raw_list:
            plant = self.create_obj(data)
            p_obj_list.append(plant)

        return p_obj_list

    def _manage_info(self, plant: Plant) -> None:
        updated = False

        if not plant.description:
            plant.description = self.chatbot.ask_description(plant.name)
            updated = True

        if not plant.species:
            plant.species = self.chatbot.ask_species(plant.name)
            updated = True

        if updated:
            plant.update_modified()
            success = self.save(plant.get_dto)

            if not success:
                raise DatabaseOperationError("Error while saving plant info to DB.")

    def get_plants_by_user(self, user: ViewerUser) -> list[Plant]:

        plant_objs: list[Plant] = []
        found_ids: set[int] = set()

        for pot in user.pots:
            plant_id = pot.plant_id
            if plant_id not in found_ids:
                found_ids.add(plant_id)
                data = self.db.get_by_id(self.table, plant_id)
                if not data:
                    raise PlantSearchError(
                        f"No se encontró la planta con ID {plant_id}"
                    )
                plant = self.create_obj(data)
                plant_objs.append(plant)

        return plant_objs


instance = PlantRepository("chatbot")
