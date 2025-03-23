class PotData:
    """
    Class that represents the sensor data of the pot (humidity, temperature, and image).
    """

    def __init__(
        self,
        id: int,
        soil_humidity: float,
        air_humidity: float,
        temperature: float,
        image: str,
    ):
        """
        Initializes the data pot with humidity, temperature, and image path.
        """
        self.soil_humidity: float = soil_humidity
        self.temperature: float = temperature
        self.air_humidity: float = air_humidity
        self.image: str = image
        self.id: int = id
