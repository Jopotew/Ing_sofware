import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "..")
sys.path.append(src_path)


from models.entities.user import User
from typing import Optional
from models.repository.repository import Repository
from repositories.pot import PotRepository, instance as pot_repository


class UserRepository(Repository):

    def __init__(self, pot_repository):
        super().__init__()
        self.table = "user"
        self.pot_repository: PotRepository = pot_repository

    def get_by_username(self, username) -> User | dict:
        try:
            u = self.db.get_by_username(username)
            if u is None:
                return {
                    "Function": "get_by_username()",
                    "status": False,
                    "detail": f"No se encontró ningún usuario con username '{username}'",
                }

            pots = self.pot_repository.get_user_pots(u["id"])
            user = User(
                u["id"],
                u["username"],
                u["mail"],
                u["password"],
                pots,
                u["last_modified"],
            )
            return user

        except Exception as e:
            return {
                "Function": "get_by_username()",
                "status": False,
                "detail": f"Excepción al obtener usuario: {str(e)}",
            }

    def validate_user(self, username: str) -> bool:
        return self.db.validate_user(username)

    def create_obj(self, data: dict) -> User:
        pots = pot_repository.get_user_pots(data["id"])
        user = User(
            data["id"],
            data["username"],
            data["mail"],
            data["password"],
            pots,
            data["last_modified"],
        )
        return user

    def update_user(
        self, user: User, field: str, old_data: str, new_data: str
    ) -> bool | dict:

        db_user = self.db.get_by_username(user.username)

        if not db_user:
            raise ValueError("Usuario no encontrado en la base de datos")

        if field not in ["username", "password"]:
            return {
                "function": "update_user()",
                "status": False,
                "detail": f"Campo inválido: {field}",
            }

        if old_data != db_user[field]:
            return {
                "function": "update_user()",
                "status": False,
                "detail": f"El valor anterior de '{field}' no coincide",
            }

        if field == "username":
            user.username = new_data
        elif field == "password":
            user.password = new_data

        user.update_modified()
        success = self.db.save(user.get_dict())

        if success:
            return success

        return {
            "function": "update_user()",
            "status": False,
            "detail": "Error al guardar en la base de datos",
        }


instance = UserRepository(pot_repository)
