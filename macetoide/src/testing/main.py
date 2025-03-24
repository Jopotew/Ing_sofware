from fastapi import FastAPI, HTTPException

from macetoide.src.models.entities.pot_data import PotData
from macetoide.src.repositorys.user import instance as user_repository
from macetoide.src.repositorys.pot import instance as pot_repository
from macetoide.src.repositorys.log import instance as log_repository
from macetoide.src.repositorys.plant import instance as plant_repository
from macetoide.src.models.entities.user import User
from macetoide.src.models.entities.pot import Pot
from macetoide.src.models.entities.plant import Plant


app = FastAPI()

app.title = "Macetoide API"
app.description = (
    "API for Macetoide, a platform for sharing and checking your macetoides."
)
app.version = "0.0.1"


@app.get("/", tags=["Home"])
def home():
    return {"Retorno a Home"}


def create_user():
    user = User("juan", "maletti", "jopote", "@jopote")
    user.id = 0
    return user


def create_plant(planta):
    plant = Plant(planta)
    return plant


def create_pot_data():
    pot_data = PotData(20, 50, 60, "2222", "442424")
    return pot_data


def create_pot(planta, analiss):

    pot = Pot(
        "pot1", create_plant(), 20, user_repository.database[1], create_pot_data()
    )
    return pot


@app.post("/plants/", tags=["Plants"])
def save_plant(plant):
    new = create_plant()
    plant_repository.save(new)
    return new.get_dto()


@app.post("/pots/", tags=["Pots"])
def save_pot(pot):
    new = create_pot()
    pot_repository.save(new)
    return new.get_dto()


@app.post("/users/", tags=["Users"])
def save_user(user):
    new = create_user()
    user_repository.save(new)
    print(user_repository.database)
    return new.get_dto()


@app.post("/users/{user_id}/pots/", tags=["Pots"])
def add_new_pot(user_id: int,):
    """
    Agrega una maceta a un usuario donde el id de la maceta es el id del usuario
    1)checkear si el user id existe y esta logeado, mandando la request
    2)checkear si el pot id existe, y pertenece al user
    """



    user = user_repository.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    pot = create_pot()

    if pot.user != user:
        raise HTTPException(status_code=403, detail="Pot does not belong to user")

    user.add_pot(pot)
    return pot.get_dto()


@app.get("/users/{user_id}/pots/{pot_id}", tags=["Pots"])
def get_pot(user_id: int, pot_id: int):
    user = user_repository.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    pot = pot_repository.get_by_id(pot_id)
    if pot is None:
        raise HTTPException(status_code=404, detail="Pot not found")

    if pot.user != user:
        raise HTTPException(status_code=403, detail="Pot does not belong to user")

    return pot.get_dto()


@app.get("/users/{user_id}/pots", tags=["Users"])
def get_user(user_id):
    user = user_repository.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user.get_dto()
