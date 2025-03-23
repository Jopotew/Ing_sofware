from macetoide.src.models.entities.analisis_time import AnalysisTime
from macetoide.src.models.entities.plant import Plant
from macetoide.src.models.entities.pot import Pot
from macetoide.src.models.entities.user import User
from datetime import datetime


class PotManager:
    """
    Controller class to manage the creation and handling of Pot objects.
    """

    def __init__(self, user: User):
        """
        Initializes the PotManager with a logged-in user.

        Args:
            user (User): The logged-in user who owns the pots.
        """
        self.user: User = user
        self.pots: list[Pot] = []  # List to store created pots

    def create_plant(self, plant_name: str, species: str = None) -> Plant:
        """
        Creates a new Plant object.

        Args:
            plant_name (str): Name of the plant.
            species (str, optional): Species of the plant. Defaults to None.

        Returns:
            Plant: The created Plant object.
        """
        plant = Plant(plant_name, species)
        return plant

    def create_analysis_time(self, minutes: int = 0, hours: int = 0) -> AnalysisTime:
        """
        Creates a new AnalysisTime object.

        Args:
            minutes (int, optional): Minutes for analysis time. Defaults to 0.
            hours (int, optional): Hours for analysis time. Defaults to 0.

        Returns:
            AnalysisTime: The created AnalysisTime object.
        """
        analysis_time = AnalysisTime(minutes, hours)
        return analysis_time

    def create_pot(
        self,
        pot_name: str,
        plant_name: str,
        species: str = None,
        minutes: int = 0,
        hours: int = 0,
    ) -> Pot:
        """
        Creates a new Pot with the specified plant, analysis time, and assigns the user.

        Args:
            pot_name (str): Name of the pot.
            plant_name (str): Name of the plant.
            species (str, optional): Species of the plant. Defaults to None.
            minutes (int, optional): Minutes for analysis time. Defaults to 0.
            hours (int, optional): Hours for analysis time. Defaults to 0.

        Returns:
            Pot: The created Pot object.
        """
        # Create the Plant object
        plant = self.create_plant(plant_name, species)

        # Create the AnalysisTime object
        analysis_time = self.create_analysis_time(minutes, hours)

        # Create the Pot object and initialize last_checked
        pot = Pot(pot_name, plant, analysis_time, self.user)
        pot.last_checked = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Optionally store the pot in a list if you want to manage multiple
        self.pots.append(pot)

        return pot

    def get_pot(self, id):
        anal = AnalysisTime(0, 0)
        return Pot("MAcetita", "tulipan", anal, self.user)
