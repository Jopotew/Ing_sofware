


from macetoide.src.models.entities.user import User


class AdminUser(User):
    def __init__(self, id: int, username: str, mail: str, password: str):
        super().__init__(id, username, mail, password)
        self.admin_role = True  


   