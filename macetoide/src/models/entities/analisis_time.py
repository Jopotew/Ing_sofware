from src.models.entities.entity import Entity
class AnalysisTime(Entity):
    """
    Class that represents the analysis time interval for the pot system.
    """

    def __init__(self,id:int, minutes: int = 0, hours: int = 0):
        """
        Initializes the analysis time, converting the total time into HH:MM:SS format.
        """

        self.total_minutes = (hours * 60) + minutes
        self.id: int = id

        total_hours = self.total_minutes // 60
        remaining_minutes = self.total_minutes % 60
        self.time = f"{total_hours:02d}:{remaining_minutes:02d}:00"
