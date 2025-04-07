import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "..")
sys.path.append(src_path)


from models.entities.user import User
from models.database.database import database as db
from models.server_credentials.security import verify_password
from typing import Optional
import bcrypt

from models.repository.repository import Repository


class UserRepository(Repository):

    def __init__(self):
        super().__init__()
        self.table = "user"

    def get_by_username(self, username) -> User:
        u = db.get_by_username(username)
        print("USER REPO U :"u)
        if u is None:
            return None
        pots = db.get_user_pots(u["id"])
        user = User(u[0]["id_user"], u[0]["username"], u[0]["mail"], u[0]["password"], pots)
        return user
     

    def new():
        pass
    
    def create_user(self, dict):
        user = User(dict[0]["id_user"], dict[0]["username"], dict[0]["mail"], dict[0]["password"])
        return user

    def update_user(self, user_id, field, old_data, new_data):
        return db.update_user(user_id, field, old_data, new_data)
    
    

instance = UserRepository()

