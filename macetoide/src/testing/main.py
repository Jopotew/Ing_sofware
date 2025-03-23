from fastapi import FastAPI, HTTPException

from macetoide.src.repositorys.user import instance as user_repository
from macetoide.src.repositorys.pot import instance as pot_repository
from macetoide.src.repositorys.log import instance as log_repository
from macetoide.src.repositorys.plant import instance as plant_repository



app = FastAPI()

app.title = "Macetoide API"
app.description = (
    "API for Macetoide, a platform for sharing and checking your macetoides."
)
app.version = "0.0.1"


@app.get("/", tags=["Home"])
def home():
    return {"Retorno a Home"}




@app.get("/users/{user_id}/pots/{pot_id}", tags=["Pots"])
def get_pot(user_id, pot_id):
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









