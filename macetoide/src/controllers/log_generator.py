# Se asume que las clases Pot, PotData, ExpertAdvice, IrrigationEvent y Log
# ya están definidas en el contexto del proyecto.

from macetoide.src.controllers.raspberry import RaspberryControll
from macetoide.src.models.entities.expert_advice import ExpertAdvice
from macetoide.src.models.entities.irrigation_event import IrrigationEvent
from macetoide.src.models.entities.log import Log
from macetoide.src.models.entities.pot_data import PotData


class LogGenerator:
    """
    Clase para generar un registro (Log) completo de una maceta seleccionada.

    Esta clase utiliza sensores conectados a una Raspberry Pi (a través de la clase
    RaspberryControll) para obtener datos actuales de la maceta (humedad del suelo,
    humedad del aire, temperatura ambiente e imagen de la planta). Con esos datos,
    crea objetos de datos y recomendaciones (PotData, ExpertAdvice). Si la humedad
    del suelo está por debajo de un cierto umbral, activa el riego automático con
    un servomotor y registra un evento de riego (IrrigationEvent). Finalmente,
    compila toda la información en un objeto Log que resume el estado de la maceta
    en ese momento.
    """

    # Umbral de humedad de suelo (%) para activar riego automático
    THRESHOLD_SOIL_HUMIDITY = 30

    def __init__(self, pot, raspbi_controller=None):
        """
        Inicializa el generador de logs para una maceta específica.

        Parámetros:
            pot (Pot): Objeto de la maceta para la cual se generará el log.
            raspbi_controller (RaspberryControll, opcional): Instancia de la clase de control
                de Raspberry Pi para acceder a sensores y actuadores. Si no se proporciona,
                se creará una nueva instancia dentro de la clase.
        """
        self.pot = pot

        if raspbi_controller is None:
            self.raspbi_controller = RaspberryControll()
        else:
            self.raspbi_controller = raspbi_controller

        self.log = None

    def generate_log(self):
        """
        Genera el objeto Log completo realizando las lecturas de sensores,
        activando el riego si es necesario, y compilando toda la información.

        Retorna:
            Log: Objeto de tipo Log que contiene la información de la maceta,
                 los datos sensoriales, el consejo experto y el evento de riego.
        """
        # 1. Obtener lecturas de los sensores mediante RaspberryControll
        soil_humidity = (
            self.raspbi_controller.read_soil_humidity()
        )  # Humedad del suelo (%)
        air_humidity, temperature = (
            self.raspbi_controller.read_dht11()
        )  # Humedad del aire (%) y temperatura (°C)
        image = self.raspbi_controller.capture_image()  # Captura de imagen de la planta

        # 2. Crear el objeto PotData con las lecturas obtenidas
        pot_data = PotData(
            soil_humidity=soil_humidity,
            air_humidity=air_humidity,
            temperature=temperature,
            image=image,
        )

        # 3. Generar el consejo experto basándose en los datos de la maceta
        expert_advice = ExpertAdvice.get_detail(pot_data)

        # 4. Verificar la necesidad de riego según la humedad del suelo
        watered = False
        duration = 0
        if soil_humidity < LogGenerator.THRESHOLD_SOIL_HUMIDITY:
            # Activar el riego automático mediante el servo
            duration = 5
            self.raspbi_controller.water_plants(duration=5)
            watered = True

        # 5. Crear el evento de riego con la información recopilada
        irrigation_event = IrrigationEvent(watered=watered, duration=duration)

        # 6. Crear el objeto Log con toda la información (maceta, datos, consejo, riego)
        log_entry = Log(
            pot=self.pot,
            data=pot_data,
            advice=expert_advice,
            irrigation=irrigation_event,
        )

        # 7. Almacenar el log generado en el atributo de la instancia y devolverlo
        self.log = log_entry
        return log_entry

    def save_log(self):
        """
        Guarda el log generado en almacenamiento persistente (por ejemplo, una base de datos).

        Este método es opcional y su implementación concreta dependerá de dónde y cómo se quieran
        almacenar los logs. Aquí se deja preparado para su futura implementación.
        """
        if self.log is None:
            print(
                "No hay ningún log generado para guardar. Por favor, genere el log primero."
            )
            return

        # Lógica de base de datos pendiente.
        # Simulamos el guardado con un mensaje o podría lanzarse una excepción NotImplementedError.
        print(
            f"Guardando el log de la maceta '{self.pot}' en la base de datos... (simulación)"
        )
        print(self.log.generate_summary())
