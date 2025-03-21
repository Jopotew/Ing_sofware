import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "..")
sys.path.append(src_path)

from providers.raspberry_components import led_component
from models.led import Led

from models.dht11 import DHT11Sensor
from providers.raspberry_components import dht11


class RaspbiComponents:
    @staticmethod
    def set_up_leds() -> list:
        """
        Sets up the LEDs connected to GPIO pins and returns a list of Led objects.
        Iterates through the led_component configuration and creates a Led instance for each.
        """
        leds = []
        for item in led_component:
            led = Led(item["component"], item["colour"], item["pin"], item["function"])
            leds.append(led)
        return leds

    @staticmethod  #No puedo probarla hasta que se intale en la raspi por el pip install 
    def set_up_dht11() -> list:
        """
        Sets up the DHT11 sensors connected to GPIO pins and returns a list of DHT11Sensor objects.
        Iterates through the dht11 configuration and creates a DHT11Sensor instance for each.
        """
        sensors = []  
        for item in dht11:
            sensor = DHT11Sensor(item["pin"])
            sensors.append(sensor)
        return sensors


r = RaspbiComponents
a = r.set_up_leds()

print(a)
