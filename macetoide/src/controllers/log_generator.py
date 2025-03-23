# Se asume que las clases Pot, PotData, ExpertAdvice, IrrigationEvent y Log
# ya están definidas en el contexto del proyecto.

#from macetoide.src.controllers.raspberry import RaspberryControll
from macetoide.src.models.entities.expert_advice import ExpertAdvice
from macetoide.src.models.entities.irrigation_event import IrrigationEvent
from macetoide.src.models.entities.log import Log
from macetoide.src.models.entities.pot import Pot
from macetoide.src.models.entities.pot_data import PotData


class LogGenerator:
    def __init__(self, pot: Pot):
        self.pot = pot



    def generate_log(self) -> Log:

        pot_data = PotData(22, 24, 25, "image_path")
        expert_advice = ExpertAdvice().get_fake_detail()
        irrigation_event = IrrigationEvent(10, True)

        return Log(self.pot, pot_data, expert_advice, irrigation_event) 