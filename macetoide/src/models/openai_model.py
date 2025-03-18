import openai
import os
import json

from pathlib import Path
from dotenv import load_dotenv

# Cargar las variables de entorno del archivo .env
load_dotenv()


class OpenAIChatbot:
    """
    Clase OpenAIChatbot para interactuar con la API de OpenAI.

    Atributos:
        api_key (str): Clave de API de OpenAI.
        system_prompt (str): Mensaje del sistema que define el estilo de las respuestas.
        history (list): Historial de mensajes de la conversación.
    """

    def __init__(
        self,
    ):
        """
        Inicializa el chatbot con API Key y configuración de TTS.

        Args:
            system_prompt (str, opcional): Mensaje de sistema para definir el tono de las respuestas.
            audio_folder (Path, opcional): Carpeta donde se guardarán los audios.
        """
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("No se encontró la API_KEY en las variables de entorno.")

        openai.api_key = self.api_key  # Configura la API Key

        self.system_prompt = """
                            Eres un científico experto especializado en Macetología llamado Marcelo Larrondo Tercero Serrano Martinez.
                            Estudias la humedad y la temperatura de la tierra de las macetas. 
                            Tu misión es redactar una “nota científica” con humor sobre el estado de la tierra, basándote en los 
                            valores de humedad y temperatura que te envía el usuario.

                            Instrucciones específicas:
                            - Di si la tierra está poco húmeda, húmeda o muy húmeda.
                            - Comenta si la temperatura es baja, media o alta para la planta.
                            - Eres arrogante ya que eres el mejor experto en Macetologia y debes hacerlo notar. 
                            - Usa un tono cómico con chistes relacionados a macetas, plantas, fútbol, mate y League of Legends.
                            - Emplea lunfardos argentinos donde sea adecuado.
                            - Combina el humor con la seriedad de un experto.

                            Responde siempre con brevedad, pero suficiente detalle para que se entienda la recomendación científica.
                            No debes exederte de los 350 caracteres, si tu respuesta inicial lo supera, seras penalizado en la revista. 
                            """

        self.history = [{"role": "system", "content": self.system_prompt}]

    def ask(
        self, user_message: str, temperature: float = 0.7, max_tokens: int = 350
    ) -> str:
        """
        Envía un mensaje del usuario a la API de OpenAI y devuelve la respuesta generada.

        Args:
            user_message (str): Mensaje del usuario.
            temperature (float, opcional): Controla la aleatoriedad de la respuesta.
            max_tokens (int, opcional): Número máximo de tokens en la respuesta.

        Returns:
            str: Respuesta generada por ChatGPT.
        """
        if not user_message:
            raise ValueError("El mensaje del usuario no puede estar vacío.")

        self.history.append({"role": "user", "content": user_message})

        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=self.history,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        answer = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": answer})

        completion_tokens = response.usage.completion_tokens

        print(f"Tokens usados en la respuesta: {completion_tokens}")

        return answer






gpt = OpenAIChatbot()
print(gpt.ask("35 °C,  humedad >= 70 %  "))