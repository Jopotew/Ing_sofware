class DataPot:
    """
    Class that represents the sensor data of the pot (humidity, temperature, and image).
    """

    def __init__(self, humidity: float, temperature: float, image: str):
        """
        Initializes the data pot with humidity, temperature, and image path.
        """
        self.humidity = humidity          
        self.temperature = temperature    
        self.image = image               
