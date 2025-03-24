from macetoide.src.models.entities.open_ai_api import Chatbot


class Plant:
    """
    Class that represents a plant in the pot system.
    """

    def __init__(self, name: str, species: str = None):
        """
        Initializes a new plant with its name, species, and an optional description.
        """
        self.id: int = None
        self.name: str = name
        self.species: str = species
        self.description: str = ""
        #self.manage_info()

    def manage_info(self):
        chatbot = Chatbot()
        if self.species == None:
            self._update_species(chatbot.ask_species(self.name))

        self._update_description(chatbot.ask_description(self.name, self.species))

    def _update_description(self, new_description: str):
        """
        Updates the plant's description.
        """
        self.description = new_description

    def _update_species(self, new_species: str):
        """
        Updates the plant's species.
        """
        self.species = new_species
