import RPi.GPIO as GPIO

class LEDData:
    """
    Data model representing the state of an LED (on/off).
    """

    def __init__(self, led_state: str):
        """
        Initialize the LEDData object with a given state.

        :param led_state: A string indicating the LED state, e.g., "ON" or "OFF".
        """
        self.led_state = led_state


class LEDController:
    """
    Controller for an LED connected to a Raspberry Pi's GPIO pin.
    Provides methods to turn the LED on or off and returns LEDData objects.
    """

    def __init__(self, led_pin: int):
        """
        Initialize the LEDController by setting up the specified GPIO pin as output.

        :param led_pin: The GPIO pin number where the LED is connected.
        """
        self.led_pin = led_pin
        GPIO.setmode(GPIO.BCM)  # or GPIO.BOARD if you use board numbering
        GPIO.setup(self.led_pin, GPIO.OUT)
        self._current_state = LEDData("OFF")

    def turn_on(self) -> LEDData:
        """
        Turn the LED on and return an LEDData object indicating the current state.

        :return: LEDData object with state set to "ON".
        """
        GPIO.output(self.led_pin, GPIO.HIGH)
        self._current_state = LEDData("ON")
        return self._current_state

    def turn_off(self) -> LEDData:
        """
        Turn the LED off and return an LEDData object indicating the current state.

        :return: LEDData object with state set to "OFF".
        """
        GPIO.output(self.led_pin, GPIO.LOW)
        self._current_state = LEDData("OFF")
        return self._current_state

    def get_state(self) -> LEDData:
        """
        Retrieve the current LED state as an LEDData object.

        :return: The current LEDData object (ON/OFF).
        """
        return self._current_state
