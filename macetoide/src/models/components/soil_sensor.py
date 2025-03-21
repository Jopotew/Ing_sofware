import RPi.GPIO as GPIO
import time

class SoilMoistureSensor:
    """
    Clase para manejar un sensor de humedad de suelo conectado al ADC0834.
    La clase inicializa y controla el ADC internamente.
    """
    def __init__(self, component: str, function: str, pin_cs: int, pin_clk: int, pin_dio: int):
        # Pines de control del ADC0834

        self.component = component
        self.function = function


        self.pin_cs = pin_cs
        self.pin_clk = pin_clk
        self.pin_dio = pin_dio

        # Canal del ADC donde está conectado el sensor
        self.channel = 0

        # Configuración de los pines
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_cs, GPIO.OUT)
        GPIO.setup(self.pin_clk, GPIO.OUT)
        GPIO.setup(self.pin_dio, GPIO.OUT)

        # Estado inicial
        GPIO.output(self.pin_cs, 1)
        GPIO.output(self.pin_clk, 0)

    def read_raw_value(self):
        """
        Lee el valor crudo (0-255) de humedad desde el ADC0834.
        """
        if self.channel < 0 or self.channel > 3:
            raise ValueError("El canal debe estar entre 0 y 3")

        # Activar el ADC
        GPIO.output(self.pin_cs, 0)
        time.sleep(0.001)

        # Enviar secuencia de inicio y selección de canal
        GPIO.output(self.pin_clk, 0)
        self._send_bit(1)  # Start bit
        self._send_bit(1)  # Single-ended mode
        self._send_bit((self.channel >> 1) & 1)  # D1
        self._send_bit(self.channel & 1)         # D0

        # Cambiar DIO a modo lectura
        GPIO.setup(self.pin_dio, GPIO.IN)

        # Leer los 8 bits de datos
        result = 0
        for _ in range(8):
            GPIO.output(self.pin_clk, 1)
            time.sleep(0.001)
            bit = GPIO.input(self.pin_dio)
            result = (result << 1) | bit
            GPIO.output(self.pin_clk, 0)
            time.sleep(0.001)

        # Terminar lectura
        GPIO.output(self.pin_cs, 1)
        GPIO.setup(self.pin_dio, GPIO.OUT)

        return result

    def _send_bit(self, bit):
        """
        Envía un bit al ADC0834 por el pin DIO.
        """
        GPIO.output(self.pin_dio, bit)
        GPIO.output(self.pin_clk, 1)
        time.sleep(0.001)
        GPIO.output(self.pin_clk, 0)
        time.sleep(0.001)

    def read_percentage(self):
        """
        Convierte el valor crudo a porcentaje de humedad (0% - 100%).
        """
        raw = self.read_raw_value()
        percentage = (raw / 255.0) * 100
        return round(percentage, 2)

    def cleanup(self):
        """
        Limpia los pines GPIO utilizados.
        """
        GPIO.cleanup()


