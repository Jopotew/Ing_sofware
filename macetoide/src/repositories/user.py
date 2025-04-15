import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "..")
sys.path.append(src_path)

from exceptions.exceptions import (
    UserNotFoundError,
    UserFieldValidationError,
    DatabaseOperationError,
)
from typing import Union
from models.entities.viewer_user import ViewerUser
from models.entities.admin_user import AdminUser
from models.repository.repository import Repository
from repositories.pot import PotRepository, instance as pot_repository
from repositories.log import LogRepository, instance as log_repository


class UserRepository(Repository):
    def __init__(self, pot_repository: PotRepository, log_repository: LogRepository):
        super().__init__()
        self.table = "user"
        self.pot_repository = pot_repository
        self.log_repository = log_repository

    def get_by_username(self, username) -> ViewerUser | AdminUser:
        try:
            u = self.db.get_by_username(username)
        except Exception as e:
            raise DatabaseOperationError(f"Exception during get_by_username: {e}")

        if u is None:
            raise UserNotFoundError(f"No user found with username '{username}'")

        pots = self.pot_repository.get_user_pots(u["id"])

        if u.get("admin_role") == True:
            return AdminUser(u["id"], u["username"], u["mail"], u["password"])
        else:
            viewer = ViewerUser(u["id"], u["username"], u["mail"], u["password"])
            viewer.pots = pots
            return viewer

    def validate_user(self, username: str) -> bool:
        return self.db.validate_user(username)

    def create_obj(self, data: dict) -> ViewerUser | AdminUser:
        pots = self.pot_repository.get_user_pots(data["id"])

        if data.get("admin_role") == True:
            return AdminUser(
                data["id"], data["username"], data["mail"], data["password"]
            )
        else:
            viewer = ViewerUser(
                data["id"], data["username"], data["mail"], data["password"]
            )
            viewer.pots = pots
            return viewer

    def delete_by_username(self, username: str) -> bool:
        success = self.db.delete_by_username(username)

        if not success:
            raise UserNotFoundError(f"Usuario '{username}' no encontrado.")

        return True

    def update_user(
        self, user: ViewerUser | AdminUser, field: str, old_data: str, new_data: str
    ) -> bool:
        db_user = self.db.get_by_username(user.username)

        if not db_user:
            raise UserNotFoundError("User not found in database")

        if field not in ["username", "password", "mail"]:
            raise UserFieldValidationError(f"Invalid field: {field}")

        if old_data != db_user[field]:
            raise UserFieldValidationError(f"Old value for '{field}' does not match")

        if field == "username":
            user.username = new_data
        elif field == "password":
            user.password = new_data
        elif field == "mail":
            user.mail = new_data

        user.update_modified()
        success = self.db.save(user.get_dict(), self.table)

        if not success:
            raise DatabaseOperationError("Failed to save updated user to database")

        return True

    def get_system_stats(self) -> dict:
        total_users = len(self.get_all())
        total_pots = len(self.pot_repository.get_all())
        total_logs = len(self.log_repository.get_all())

        return {"users": total_users, "pots": total_pots, "logs": total_logs}


instance = UserRepository(pot_repository, log_repository)
