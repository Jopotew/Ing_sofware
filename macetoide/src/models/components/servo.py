from gpiozero import Servo
from time import sleep

class Servo:
    """
    Model for controlling a servo motor connected to a Raspberry Pi GPIO pin using gpiozero.
    Allows setting angles between 0° and 180°.
    """

    def __init__(self, component: str, function: str, pin: int):
        """
        Initialize the ServoMotor with gpiozero Servo object.

        :param servo_pin: The GPIO pin number where the servo's signal line is connected.
        """

        self.component = component
        self.function = function
        self.servo = Servo(pin, min_pulse_width=0.0005, max_pulse_width=0.0025)

    def set_angle(self, angle: float):
        """
        Move the servo motor to the specified angle (0° to 180°).
        Converts angle to the -1 to 1 range used by gpiozero.

        :param angle: The target angle in degrees (0 to 180).
        """
        if not 0 <= angle <= 180:
            raise ValueError("Angle must be between 0 and 180 degrees.")

        # Convert 0-180 degrees to -1 to 1 for gpiozero
        servo_value = (angle / 90.0) - 1 
        self.servo.value = servo_value
        sleep(0.5)  
