from macetoide.src.models.entities.user import User
from macetoide.src.models.entities.database import Database
from typing import Optional


class UserManagment:

    def __init__(self):
        self.user: User

    def login(self, username: str, password: str) -> Optional[User]:
        db = Database()
        if self._search_username(username, db) and self._search_password(password, db):
            self.user = self._create_user(db)
            return self.user
        return None

    def _search_username(self, username: str, db: Database) -> bool:

        return True

    def _search_password(self, password: str, db: Database) -> bool:
        return True

    def _create_user(self) -> User:
        user = User("Juan", "maletti", "Jopote", "dd@.com",  )
        return user


    def get_user(self, id):
        return  User("Juan", "maletti", "Jopote", "dd@.com",  )
    
    def change_username(self, new_username):
        self.user.change_username(new_username)

    def change_password(self, new_password):
        self.user.change_password(new_password)
