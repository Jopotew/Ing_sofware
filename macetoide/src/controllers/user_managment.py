from models.entities.user import User
from models.entities.database import Database
from typing import Optional

class UserManagment():
    
    def __init__(self):
        self.user: User 

    def login(self, username: str, password: str) -> Optional[User]:
        db = Database()
        if self._search_username(username, db) and self._search_password(password, db):
            self.user = self._create_user(db)
            return self.user
        return None

    def _search_username(self, username: str, db: Database) -> bool:
        return db.search_username(username)

    def _search_password(self, password: str, db: Database) -> bool:
        return db.search_password(password)

    def _create_user(self, db: Database) -> User:
        return db.search_user()

    def change_username(self, new_username):
        self.user.change_username(new_username)

    def change_password(self, new_password):
        self.user.change_password(new_password)