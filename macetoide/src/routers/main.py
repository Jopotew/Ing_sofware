import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "..")
sys.path.append(src_path)


from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from routers import auth, user, pot, log, plant
import threading

print(dir(threading))

from services.log_scheduler import LogScheduler
from exceptions.exceptions import (
    RepositoryError,
    UserNotFoundError,
    UserFieldValidationError,
    DatabaseOperationError,
    PotNotFoundError,
    LogDataFetchError,
    PlantSearchError,
)


app = FastAPI()
app.title = "Macetoide API"
app.description = (
    "API for Macetoide, a platform for sharing and checking your macetoides."
)
app.version = "0.69"


@app.exception_handler(UserNotFoundError)
@app.exception_handler(PotNotFoundError)
@app.exception_handler(LogDataFetchError)
@app.exception_handler(PlantSearchError)
async def not_found_handler(request: Request, exc: RepositoryError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)}
    )


@app.exception_handler(UserFieldValidationError)
async def validation_error_handler(request: Request, exc: UserFieldValidationError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)}
    )


@app.exception_handler(DatabaseOperationError)
async def db_error_handler(request: Request, exc: RepositoryError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": str(exc)}
    )


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(pot.router)
app.include_router(log.router)
app.include_router(plant.router)


@app.get("/")
def root_status():
    return {
        "status": "ok",
        "title": app.title,
        "version": app.version,
        "description": app.description,
        "message": "Bienvenido a la API de Macetoide 🌱",
    }


scheduler = LogScheduler()


def schedule_log_check():
    scheduler.run()
    t= threading.Timer(60, schedule_log_check)
    t.start()
    print("start")

schedule_log_check()
