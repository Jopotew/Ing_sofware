from datetime import datetime
from pydantic import BaseModel


class LoginForm(BaseModel):
    username: str
    password: str


class UserForm(BaseModel):
    id: int
    username: str
    mail: str
    password: str

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "mail": self.mail,
            "password": self.password,
        }


class RegisterForm(UserForm):
    pass


class PotForm(BaseModel):
    id: int
    name: str
    id_plant: int
    analysis_time: str
    id_user: int
    last_checked: str

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "id_plant": self.id_plant,
            "analysis_time": self.analysis_time,
            "id_user": self.id_user,
            "last_checked": self.last_checked,
        }


class PlantForm(BaseModel):
    id: int
    name: str
    scpecies: str
    description: str

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "species": self.scpecies,
            "description": self.description,
        }


class LogForm(BaseModel):
    id: int
    pot_id: int
    plant_id: int
    temperature: float
    soil_humidity: float
    air_humidity: float
    image_path: str
    expert_advice: str
    timestamp: datetime


class AdminRegisterForm(BaseModel):
    username: str
    mail: str
    password: str
    admin_role: bool = False


    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "mail": self.mail,
            "password": self.password,
            "admin_role": self.admin_role,
        }

class DataUpdateForm(BaseModel):
    old_data: str
    new_data: str

    




















