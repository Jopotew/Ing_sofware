from macetoide.src.models.entities.open_ai_api import PlantAssistant
from macetoide.src.models.entities.pot_data import PotData


class ExpertAdvice:
    """
    Class that stores the expert advice given by the OpenAI chatbot.
    """

    def __init__(self, id: int):
        """
        Initializes the expert advice with the OpenAI response.
        """

        self.detail: str = ""
        self.id: int = id

    def get_detail(self, pot_data: PotData):
        assistant = PlantAssistant()

        temp = pot_data.temperature
        soil_humidity = pot_data.soil_humidity
        air_humidity = pot_data.air_humidity

        self.detail(assistant.get_recommendation(temp, soil_humidity, air_humidity))
        return self.detail
    
    def get_fake_detail(self):
        return "This is a fake detail for testing purposes."
