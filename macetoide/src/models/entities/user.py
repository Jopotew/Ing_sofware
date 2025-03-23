from macetoide.src.models.entities.database import Database


class User:
    """
    Clase que representa a un usuario con manejo de codificación UTF-8 para la contraseña.
    """

    def __init__(
        self,
        id: int,
        name: str,
        surname: str,
        username: str,
        mail: str,
    ):
        """
        Inicializa un nuevo usuario con los datos proporcionados.
        """
        self.id: int = id
        self.name = name
        self.surname = surname
        self.username = username
        self.mail = mail
        self.pots = []

    def change_username(self, new_username):
        db = Database()
        db.change_user_username(self.id, new_username)

    def change_password(self, new_password):
        db = Database()
        db.change_user_password(self.id, new_password)

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

    
