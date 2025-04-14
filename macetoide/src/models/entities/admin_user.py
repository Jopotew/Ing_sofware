


from models.entities.user import User


class AdminUser(User):
    def __init__(self, id: int, username: str, mail: str, password: str):
        super().__init__(id, username, mail, password)
        self.admin_role = True  


    def get_dto(self):
        return {
            "id": self.id,
            "username": self.username,
            "mail": self.mail,
            "role": "admin"
        }