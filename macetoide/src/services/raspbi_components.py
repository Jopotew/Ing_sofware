import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "..")
sys.path.append(src_path)

from macetoide.src.models.components.servo import Servo
from providers.raspberry_components import led_component, dht11, soil_sensor, servo_list
from macetoide.src.models.components.led import Led
from macetoide.src.models.components.dht11 import DHT11Sensor
from macetoide.src.models.components.soil_sensor import SoilMoistureSensor
from macetoide.src.models.components.camera import Camera


class RaspbiComponents:
    @staticmethod
    def set_up_leds() -> list[Led]:
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
    def set_up_dht11() -> DHT11Sensor:
        """
        Sets up the DHT11 sensors connected to GPIO pins and returns a list of DHT11Sensor objects.
        Iterates through the dht11 configuration and creates a DHT11Sensor instance for each.
        """ 
        for item in dht11:
            sensor = DHT11Sensor(item["component"],item["function"],item["pin"])
        return sensor


    def set_up_soil_sensor() -> SoilMoistureSensor:
        for item in soil_sensor:
            sensor = SoilMoistureSensor(item["component"], item["function"], item["pin_cs"], item["pin_clk"], item["pin_dio"])
        return sensor
    

    def set_up_servo() -> Servo:
        for item in servo_list:
            servo = Servo(item["component"], item["function"], item["pin"])
        return servo
            
            
    def set_up_camera()-> Camera:
        return Camera()
        











