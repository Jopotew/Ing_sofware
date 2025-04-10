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
from models.entities.user import User
from models.repository.repository import Repository
from repositories.pot import PotRepository, instance as pot_repository


class UserRepository(Repository):
    def __init__(self, pot_repository: PotRepository):
        super().__init__()
        self.table = "user"
        self.pot_repository = pot_repository

    def get_by_username(self, username) -> User:
        try:
            u = self.db.get_by_username(username)
        except Exception as e:
            raise DatabaseOperationError(f"Exception during get_by_username: {e}")

        if u is None:
            raise UserNotFoundError(f"No user found with username '{username}'")

        pots = self.pot_repository.get_user_pots(u["id"])
        return User(
            u["id"],
            u["username"],
            u["mail"],
            u["password"],
            pots,
            u["last_modified"],
        )

    def validate_user(self, username: str) -> bool:
        return self.db.validate_user(username)

    def create_obj(self, data: dict) -> User:
        pots = self.pot_repository.get_user_pots(data["id"])
        return User(
            data["id"],
            data["username"],
            data["mail"],
            data["password"],
            pots,
            data["last_modified"],
        )

    def update_user(self, user: User, field: str, old_data: str, new_data: str) -> bool:
        db_user = self.db.get_by_username(user.username)

        if not db_user:
            raise UserNotFoundError("User not found in database")

        if field not in ["username", "password"]:
            raise UserFieldValidationError(f"Invalid field: {field}")

        if old_data != db_user[field]:
            raise UserFieldValidationError(f"Old value for '{field}' does not match")

        if field == "username":
            user.username = new_data
        elif field == "password":
            user.password = new_data

        user.update_modified()
        success = self.db.save(user.get_dict())

        if not success:
            raise DatabaseOperationError("Failed to save updated user to database")

        return True


instance = UserRepository(pot_repository)
