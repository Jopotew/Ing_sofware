import openai
import os
import json
import time

from pathlib import Path
from dotenv import load_dotenv


load_dotenv()


class PlantAssistant:

    def __init__(self):
       
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.assistant_id = "asst_qysrgPulnpfwd76CsDwMLCZZ".strip()
        openai.api_key = self.api_key


    def get_recommendation(
        self, temperature: float, soil_humidity: float, air_humidity: float
    ) -> str:

        try:
            thread = openai.beta.threads.create()
            message = f"Temperatura: {temperature}°C\nHumedad del Suelo: {soil_humidity}%\nHumedad del aire: {air_humidity}%"

            openai.beta.threads.messages.create(
                thread_id=thread.id, role="user", content=message
            )

            run = openai.beta.threads.runs.create(
                thread_id=thread.id, assistant_id=self.assistant_id
            )

            while True:
                run_status = openai.beta.threads.runs.retrieve(
                    thread_id=thread.id, run_id=run.id
                )
                if run_status.status == "completed":
                    break
                elif run_status.status in ["failed", "cancelled"]:
                    return "Error: La ejecución del asistente falló."
                time.sleep(1)  
           
            messages = openai.beta.threads.messages.list(thread_id=thread.id)

            for msg in messages.data:
                if msg.role == "assistant":
                    return msg.content[0].text.value.strip()

            return "No se recibió respuesta del asistente."

        except Exception as e:
            return f"Error al obtener la recomendación: {str(e)}"


class Chatbot:
    def __init__(
        self,
    ):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("No se encontró la API_KEY en las variables de entorno.")

        openai.api_key = self.api_key  

        self.system_prompt = """
                            Eres un científico experto especializado en Macetología llamado Marcelo Larrondo Tercero Serrano Martinez.
                            Estudias la humedad y la temperatura de la tierra de las macetas. 
                            Tu misión es redactar una “nota científica” con humor sobre el estado de la tierra, basándote en los 
                            valores de humedad y temperatura que te envía el usuario.

                            Instrucciones específicas:
                            - Di si la tierra está poco húmeda, húmeda o muy húmeda.
                            - Comenta si la temperatura es baja, media o alta para la planta.
                            - Eres arrogante ya que eres el mejor experto en Macetologia y debes hacerlo notar.
                            - Puedes humillar al cuidador de la maceta si hace falta. 
                            - Usa un tono cómico con chistes relacionados a macetas, plantas, fútbol.
                            - Emplea lunfardos argentinos donde sea adecuado.
                            - Combina el humor con la seriedad de un experto.

                            Responde siempre con brevedad, pero suficiente detalle para que se entienda la recomendación científica.
                            No debes exederte de los 450 caracteres, si tu respuesta inicial lo supera, seras penalizado en la revista. 
                            """

        self.history = [{"role": "system", "content": self.system_prompt}]

    def ask(
        self, user_message: str, temperature: float = 0.7, max_tokens: int = 350
    ) -> str:
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


    def ask_species(self, plant_name: str) -> str:

        prompt = (
            f"Dime la especie científica de la planta llamada '{plant_name}'. "
            f"Solo responde el nombre de la especie, sin explicaciones ni detalles extras."
        )

        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=self.history + [{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=50,
        )

        species = response.choices[0].message.content.strip()
        return species


    def ask_description(self, plant_name: str, species: str) -> str:
        prompt = (
            f"Genera una descripción científica sobre la planta '{plant_name}' "
            f"de la especie '{species}'. No uses más de 350 caracteres."
        )

        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=self.history + [{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=350,
        )

        description = response.choices[0].message.content.strip()
        return description


# instance_chatbot = Chatbot() 
# instance_assistant = PlantAssistant()
