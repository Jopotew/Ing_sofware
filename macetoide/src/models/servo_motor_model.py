import RPi.GPIO as GPIO

class ServoMotor:
    """
    Model for controlling a servo motor connected to a Raspberry Pi GPIO pin via PWM.
    """

    def __init__(self, servo_pin: int, frequency: int = 50):
        """
        Initialize the ServoMotor by setting up the GPIO pin and PWM.

        :param servo_pin: The GPIO pin number where the servo's signal line is connected.
        :param frequency: The PWM frequency, typically 50Hz for most servo motors.
        """
        self.servo_pin = servo_pin
        self.frequency = frequency

        GPIO.setmode(GPIO.BCM)  # or GPIO.BOARD if you use board numbering
        GPIO.setup(self.servo_pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.servo_pin, self.frequency)
        self.pwm.start(0)  # Initialize PWM with 0% duty cycle

    def set_angle(self, angle: float):
        """
        Move the servo motor to the specified angle.

        :param angle: The target angle in degrees (0 to 180 for most servo motors).
        """
        # Convert angle to duty cycle (this formula may vary for specific servo calibrations).
        duty_cycle = 2 + (angle / 18)
        self.pwm.ChangeDutyCycle(duty_cycle)

    def stop(self):
        """
        Stop the PWM signal and clean up resources for the servo motor.
        """
        self.pwm.stop()
        GPIO.cleanup(self.servo_pin)
