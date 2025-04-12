import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "..")
sys.path.append(src_path)


from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routers import auth, user, pot, log, plant
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


@app.exception_handler(UserNotFoundError)
@app.exception_handler(PotNotFoundError)
@app.exception_handler(LogDataFetchError)
@app.exception_handler(PlantSearchError)
async def not_found_handler(request: Request, exc: RepositoryError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(UserFieldValidationError)
async def validation_error_handler(request: Request, exc: UserFieldValidationError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(DatabaseOperationError)
async def db_error_handler(request: Request, exc: RepositoryError):
    return JSONResponse(status_code=500, content={"detail": str(exc)})


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(pot.router)
app.include_router(log.router)
app.include_router(plant.router)
