from models.entities.open_ai_api import PlantAssistant
from macetoide.src.models.entities.data_pot import DataPot

class ExpertAdvice:
    """
    Class that stores the expert advice given by the OpenAI chatbot.
    """

    def __init__(self):
        """
        Initializes the expert advice with the OpenAI response.
        """
        self.detail: str
        self.get_detail()

    def get_detail(self, data_pot: DataPot):
        assistant = PlantAssistant()

        temp = data_pot.temperature
        humidity = data_pot.humidity
        

        self.detail(assistant.get_recommendation(temp, humidity))

          
