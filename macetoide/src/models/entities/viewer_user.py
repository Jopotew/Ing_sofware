
from models.entities.pot import Pot
from models.entities.user import User


class ViewerUser(User):
    def __init__(self, id, username, mail, password):
        super().__init__(id, username, mail, password)
        self.pots: list[Pot]

    def add_pot(self, pot):
        self.pots.append(pot)

    def get_dto(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "mail": self.mail,
            "pots": self.pots,
            "last_modified": self.last_modified,
        }