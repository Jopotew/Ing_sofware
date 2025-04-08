from models.repository.repository import Repository
from models.entities.plant import Plant

class PlantRepository(Repository):
    def __init__(self):
        super().__init__()
        self.table = "plant" 

    def create_obj(data: dict):
        plant = Plant(data["name"], data["species"], data["description"],)
        return plant

instance = PlantRepository()
 