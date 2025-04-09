from datetime import datetime
from macetoide.src.models.entities.pot import Pot


class User:
    """
    Clase que representa a un usuario con manejo de codificación UTF-8 para la contraseña.
    """

    def __init__(
        self,
        id: int,
        username: str,
        mail: str,
        password: str,
        pots: list,
        last_modified: int
    ):
        """
        Inicializa un nuevo usuario con los datos proporcionados.
        """
        self.id: int = id
        self.name: str
        self.username = username
        self.mail = mail
        self.pots: list[Pot] = pots
        self.password: str =  password
        self.last_modified: int = last_modified

 
    def add_pot(self, pot):
        self.pots.append(pot)   

    def update_modified(self):
        self.last_modified = datetime.now()   


    def get_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "password": self.password,
            "mail": self.mail,
            "last_modified": self.last_modified
        }   

    def get_dto(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "mail": self.mail, 
            "pots": self.pots,
            "last_modified": self.last_modified
        }

    
