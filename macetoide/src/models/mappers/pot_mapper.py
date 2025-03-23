import sys
import os

# Agregar el directorio `src` al path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "..")
sys.path.append(src_path)

from macetoide.src.models.dtos.pot_dto import PotDTO
from macetoide.src.models.entities.entity import Entity
from macetoide.src.models.entities.pot import Pot


class PotMapper:

    def create_dto(entity: Entity):
        return PotDTO(entity.id)

    def create_entity(dto):
        pass


pot_dto = PotMapper
pot = Pot(1, "name", "plant", "analysis_time", "user")
print(pot_dto.create_dto(Pot))
