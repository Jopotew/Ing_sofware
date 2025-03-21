from dataclasses import dataclass
from gpiozero import LED


@dataclass
class Led:
    """
    Represents an LED in the system.

    Attributes:
        led_color (str): The color of the LED (e.g., "red", "green").
        raspi_pin (LED): The GPIOZero LED instance representing the physical LED.
    """
    component: str
    led_color: str
    raspi_pin: LED
    function: str
    
    def on(self):
        """
        Turns the LED on by activating the GPIO pin.
        """
        self.raspi_pin.on()

    def off(self):
        """
        Turns the LED off by deactivating the GPIO pin.
        """
        self.raspi_pin.off()
