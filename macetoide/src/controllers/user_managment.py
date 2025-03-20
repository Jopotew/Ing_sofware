from models.user import User
from models.database import Database

class UserManagment():
    
    def __init__(self, user: User):
        self.user: User = user

    def login(self, username: str, password: str) -> bool:
        db = Database()
        if self._search_user(username, db) and self._search_password(password, Database):
            return True
        return False

    def _search_user(self, username: str, db: Database) -> bool:
        return db.search_username(username)

    def _search_password(self, password: str, db: Database) -> bool:
        return db.search_password(password)

    def change_username(self):
        pass

    def change_password(self):
        pass