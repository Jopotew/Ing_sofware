from models.pot import pot
from models.database import Database

class User:
    """
    Clase que representa a un usuario con manejo de codificación UTF-8 para la contraseña.
    """

    def __init__(self, name: str, surname: str, username: str, mail: str, password: str):
        """
        Inicializa un nuevo usuario con los datos proporcionados.
        """

        self.name = name
        self.surname = surname
        self.username = username
        self.mail = mail
        self.password = password



    def change_username(self, new_username):
        db = Database()
        db.change_user_username(new_username)

    def change_password(self, new_password):
        db = Database()
        db.change_user_password(new_password)