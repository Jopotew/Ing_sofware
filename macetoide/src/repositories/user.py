import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "..")
sys.path.append(src_path)


from models.entities.user import User
from models.server_credentials.security import verify_password
from typing import Optional
import bcrypt

from models.repository.repository import Repository
from repositories.pot import instance as pot_repository


class UserRepository(Repository):

    def __init__(self, pot_repository):
        super().__init__()
        self.table = "user"
        self.pot_repository = pot_repository

    def get_by_username(self, username) -> User:
        u = self.db.get_by_username(username)
        if u is None:
            return None
        pots = pot_repository.get_user_pots(u["id"])
        user = User(u["id"], u["username"], u["mail"], u["password"], pots)
        return user
     

    def validate_user(self, username: str):
        return self.db.validate_user(username)
    
    def create_obj(self, data: dict):
        pots = pot_repository.get_user_pots(data["id"])
        user = User(data["id"], data["username"], data["mail"], data["password"])
        return user

    def update_user(self, user_id, field, old_data, new_data):
        return self.db.update_user(user_id, field, old_data, new_data)
    
    

instance = UserRepository(pot_repository)

