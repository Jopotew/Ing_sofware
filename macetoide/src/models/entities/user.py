
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
        pots: list
    ):
        """
        Inicializa un nuevo usuario con los datos proporcionados.
        """
        self.id: int = id
        self.name: str
        self.username = username
        self.mail = mail
        self.pots: list = pots
        self.password: str =  password

 
    def add_pot(self, pot):
        self.pots.append(pot)   


    def get_dto(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "mail": self.mail, 
            "pots": self.pots,
        }

    
