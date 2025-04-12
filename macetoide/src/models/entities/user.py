from datetime import datetime


class User:
    def __init__(
        self,
        id: int,
        username: str,
        mail: str,
        password: str,
    ):
        self.id: int = id
        self.username = username
        self.mail = mail
        self.admin_role: bool = False
        self.password: str = password
        self.last_modified: datetime

    
    def update_modified(self):
        self.last_modified = datetime.now()

    def get_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "role": self.admin_role,
            "mail": self.mail,
            "last_modified": self.last_modified,
        }


