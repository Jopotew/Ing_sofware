
from datetime import time
from macetoide.src.models.components.camera import Camera, ImageData
from macetoide.src.models.components.dht11 import DHT11Sensor, DHT11Data
from macetoide.src.models.components.led import Led
from macetoide.src.models.components.servo import Servo
from macetoide.src.models.components.soil_sensor import SoilMoistureSensor
from services.raspbi_components import RaspbiComponents

class RaspberryControll:

    def __init__(self):
        self.rb = RaspbiComponents
        self.leds: list[Led]
        self.dht11: DHT11Sensor
        self.servo: Servo
        self.soil_sensor: SoilMoistureSensor
        self.camera: Camera

        self.set_lists()


    def set_components(self):
        self.leds = self.rb.set_up_leds()
        self.dht11 = self.rb.set_up_dht11()
        self.servo = self.rb.set_up_servo()
        self.soil_sensor = self.rb.set_up_soil_sensor()
        self.camera = self.rb.set_up_camera()


    def water_plants(self, duration: int):
        self.set_servo_angle(90)
        time.sleep(duration)
        self.set_servo_angle(0)


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
        

    def get_dht11_data(self) -> DHT11Data:
        return self.dht11.read_sensor_data()
                    

    def set_servo_angle(self, angle: float):
        self.servo.set_angle(angle)


    def get_camera_picture(self) -> ImageData:
        picture_data = self.camera.capture_image
        return picture_data
    

    def get_soil_data(self):
        return self.soil_sensor.read_percentage()