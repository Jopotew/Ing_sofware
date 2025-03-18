import time
from typing import Optional

# Importar las clases creadas previamente
# from dht11_sensor import DHT11Sensor, DHT11Data
# from camera_model import RaspberryPiCamera, CameraImageData
# from led_controller import LEDController, LEDData
# from servo_motor import ServoMotor


class Controller:
    """
    This Controller class orchestrates the entire process of:
    1) Reading temperature and humidity from the DHT11 sensor.
    2) Taking a photo with the Raspberry Pi camera.
    3) Turning LEDs on/off to indicate progress.
    4) Storing data in the database.
    5) Sending data to the OpenAI API to get a recommendation.
    6) (Optionally) Using the servo motor for watering if needed.
    """

    def __init__(
        self,
        dht_sensor,  # type: DHT11Sensor
        camera,  # type: RaspberryPiCamera
        led_red_controller,  # type: LEDController
        led_green_controller,  # type: LEDController
        db_service=None,  # placeholder for a DB service or connection
        openai_service=None,  # placeholder for an OpenAI API client
        servo_motor=None,  # type: Optional[ServoMotor]
    ):
        """
        Initialize the Controller with references to the sensor, camera,
        LED controllers, and optional services (database, OpenAI, servo).

        :param dht_sensor: An instance of DHT11Sensor for reading temp/humidity.
        :param camera: An instance of RaspberryPiCamera for capturing images.
        :param led_red_controller: An LEDController instance for the red LED.
        :param led_green_controller: An LEDController instance for the green LED.
        :param db_service: A placeholder for the database service.
        :param openai_service: A placeholder for interacting with the OpenAI API.
        :param servo_motor: An optional servo motor for watering if needed.
        """
        self.dht_sensor = dht_sensor
        self.camera = camera
        self.led_red = led_red_controller
        self.led_green = led_green_controller
        self.db_service = db_service
        self.openai_service = openai_service
        self.servo_motor = servo_motor

    def run_cycle(self):
        """
        Perform one cycle of the system:
        1) Turn on the red LED (process start).
        2) Read data from the DHT11 sensor.
        3) Capture a photo using the Raspberry Pi camera.
        4) Store data in the database.
        5) Send data to OpenAI API and store the response.
        6) Turn off the red LED.
        7) Turn on green LED for 5 seconds (process finished).
        8) Optionally, move the servo motor if watering is needed.
        """
        # 1) Turn on red LED
        self.led_red.turn_on()

        # 2) Read sensor data
        sensor_data = self.dht_sensor.read_sensor_data()
        temperature = sensor_data.temperature
        humidity = sensor_data.humidity

        # 3) Capture a photo
        image_data = self.camera.capture_image()

        # 4) Store data in the database (placeholder)
        #    Let's assume db_service.save_measurement is a function that takes temperature, humidity, image file path, and returns an ID.
        measurement_id = None
        if self.db_service is not None:
            measurement_id = self.db_service.save_measurement(
                temperature=temperature,
                humidity=humidity,
                image_path=image_data.file_name,
            )

        # 5) Send data to OpenAI API and store the response (placeholder)
        #    Let's assume openai_service.get_advice is a function that receives temp/humidity and returns a string advice.
        openai_advice = None
        if self.openai_service is not None:
            openai_advice = self.openai_service.get_advice(
                temperature=temperature, humidity=humidity
            )
            if openai_advice and self.db_service is not None:
                self.db_service.save_advice(measurement_id, openai_advice)

        # 6) Turn off red LED
        self.led_red.turn_off()

        # 7) Turn on green LED for ~5 seconds, then turn it off
        self.led_green.turn_on()
        time.sleep(5)
        self.led_green.turn_off()

        # 8) Optionally, check if watering is needed and use servo
        if self.servo_motor:
            # Example: if humidity < 30%, water for 2 seconds
            if humidity is not None and humidity < 30:
                # Move servo to open the water flow (angle 90 for instance)
                self.servo_motor.set_angle(90)
                time.sleep(2)
                # Return servo to closed position (angle 0)
                self.servo_motor.set_angle(0)

        # End of cycle. The system is ready for the next cycle.d
