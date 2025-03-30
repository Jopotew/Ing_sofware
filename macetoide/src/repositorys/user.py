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

    def get_by_username(self, username):
        u = db.get_by_username(username)
        if u:
            user = User(u["id"], u["username"], u["mail"], u["password"])
            return user
        return None

    def verify_user(self, username: str, password: str) -> User | None:
        users = db.execute_query("SELECT * FROM user")
        for u in users:
            if u["username"] == username and verify_password(password, u["password"]):
                return User(u["id"], u["username"], u["email"])
        return None


instance = UserRepository()
print(instance.get_by_username("juan"))
