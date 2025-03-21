#import Adafruit_DHT

class DHT11Data:
    """
    Data model representing temperature and humidity readings of the room
    from a DHT11 sensor.
    """

    def __init__(self, temperature: float, humidity: float):
        """
        Initialize the DHT11Data object with temperature and humidity.

        :param temperature: The temperature value in Celsius.
        :param humidity: The humidity value in percentage.
        """
        self.temperature = temperature
        self.humidity = humidity


class DHT11Sensor:
    """
    Model for managing a DHT11 sensor using the Adafruit_DHT library.
    This class provides a method to read temperature and humidity data
    from the sensor.
    """

    def __init__(self, pin: int):
        """
        Initialize the DHT11Sensor with the specified GPIO pin.

        :param pin: The GPIO pin number to which the DHT11 data pin is connected.
        """
        self.pin = pin

    def read_sensor_data(self) -> DHT11Data:
        """
        Read temperature and humidity data from the DHT11 sensor.

        :return: An instance of DHT11Data with the temperature and humidity readings.
        """
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, self.pin)
        # If there's an error in reading, humidity or temperature might be None, so it can be handled accordingly.
        # For now, we'll assume it always returns valid data.
        return DHT11Data(temperature, humidity)
