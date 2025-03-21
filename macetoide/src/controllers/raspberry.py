
from macetoide.src.models.components.camera import Camera
from macetoide.src.models.components.dht11 import DHT11Sensor
from macetoide.src.models.components.led import Led
from macetoide.src.models.components.servo import Servo
from macetoide.src.models.components.soil_sensor import SoilMoistureSensor
from services.raspbi_components import RaspbiComponents

class RaspberryControll:

    def __init__(self):
        self.rb = RaspbiComponents
        self.leds: list[Led]
        self.dht11: list[DHT11Sensor] # list of 1
        self.servo: list[Servo] # list of 1
        self.soil_sensor: list[SoilMoistureSensor] # list of 1
        self.camera: list[Camera] # list of 1

        self.set_lists()


    def set_lists(self):
        self.leds = self.rb.set_up_leds()
        self.dht11 = self.rb.set_up_dht11()
        self.servo = self.rb.set_up_servo_motor()
        self.soil_sensor = self.rb.set_up_soil_sensor()
        self.camera = self.rb.set_up_camera()


    def set_led_status(self, led_function: str, value: bool):
        if led_function == "completion":
            for i in self.leds:
                if i.function == "completion" and value:
                    i.on()
                elif i.function == "completion" and not value:
                    i.off()
        elif led_function == "processing":
            for i in self.leds:
                if i.function == "processing" and value:
                    i.on()
                elif i.function == "processing" and not value:
                    i.off()
        else:
            raise ValueError("Invalid led funtion")
        

    def get_dht11_data(self):
        dht11_data = []
        for i in self.dht11:
            dht11_data.append(i.read_sensor_data())
        return dht11_data[0]
                    

    def set_servo_angle(self, angle: int):
        for i in self.servo:
            i.set_angle(angle)