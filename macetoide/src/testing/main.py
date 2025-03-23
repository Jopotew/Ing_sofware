from fastapi import FastAPI, HTTPException
from macetoide.src.controllers.log_generator import LogGenerator
from macetoide.src.controllers.pot_manager import PotManager
from macetoide.src.controllers.user_managment import UserManagment

app = FastAPI()

app.title = "Macetoide API"
app.description = (
    "API for Macetoide, a platform for sharing and checking your macetoides."
)
app.version = "0.0.1"


@app.get("/", tags=["Home"])
def home():
    return {"Retorno a Home"}


user_managment = UserManagment()


class LogRepo:
    def __init__(
        self,
    ):
        self.logs = []

    def save_log(self, log):
        self.logs.append(log)


log_rep = LogRepo()


@app.post("/users/{user_id}/pots/{pot_id}/logs", tags=["Logs"])
def create_log(user_id, pot_id):
    # 1)checkear si el user id existe y esta logeado, mandando la request
    # 2)checkear si el pot id existe, y pertenece al user

    user = user_managment.get_user(user_id)
    pot_manag = PotManager(user)
    pot = pot_manag.get_pot(pot_id)

    if pot is None:
        raise HTTPException(status_code=404, detail="Pot not found")
    log_generator = LogGenerator(pot)

    log = log_generator.generate_log()

    log_rep.save_log(log)
    return log



@app.get("/users/{user_id}/pots/{pot_id}/logs", tags=["Logs"])
def get_logs(user_id, pot_id):

    return log_rep.logs







#dtos data transfer objects
#user dtos
#plant dtos
#pot dtos

class user_dto:
    def __init__(self, id: int):
        self.id = id

class plant_dto:
    def __init__(self, id: int):
        self.id = id

class pot_dto:
    def __init__(self, id: int):
        self.id = id


log={
    "pot": pot_dto,
    "pot_data": {
      "soil_humidity": 22,
      "temperature": 25,
      "air_humidity": 24,
      "image": "image_path"
    },
    "expert_advice": "This is a fake detail for testing purposes.",
    "irrigation_event": {
      "time_active": 10,
      "watered": True
    }
  },












