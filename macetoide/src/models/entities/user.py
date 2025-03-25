from macetoide.src.models.database.database import Database


class User:
    """
    Clase que representa a un usuario con manejo de codificación UTF-8 para la contraseña.
    """

    def __init__(
        self,
        name: str,
        surname: str,
        username: str,
        mail: str,
    ):
        """
        Inicializa un nuevo usuario con los datos proporcionados.
        """
        self.id: int = None
        self.name = name
        self.surname = surname
        self.username = username
        self.mail = mail
        self.pots = []
        self.password = None

 
    def add_pot(self, pot):
        self.pots.append(pot)   


    def get_dto(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname, 
            "username": self.username,
            "mail": self.mail, 
            "pots": self.pots,
        }

    
