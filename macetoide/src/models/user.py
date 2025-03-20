from models.pot import pot

class User:
    """
    Clase que representa a un usuario con manejo de codificación UTF-8 para la contraseña.
    """

    def __init__(self, nombre: str, apellido: str, username: str, correo: str, contrasenia: str):
        """
        Inicializa un nuevo usuario con los datos proporcionados y codifica la contraseña.
        """

        self.nombre = nombre
        self.apellido = apellido
        self.username = username
        self.correo = correo
        self.contrasenia = contrasenia.encode('utf-8') 

    def set_password(self, nueva_contrasenia: str):
        """
        Actualiza la contraseña del usuario, codificándola en UTF-8.
        """
        self.contrasenia = nueva_contrasenia.encode('utf-8')

    def check_password(self, contrasenia_a_validar: str) -> bool:
        """
        Valida si la contraseña ingresada coincide con la almacenada.
        """
        return self.contrasenia == contrasenia_a_validar.encode('utf-8')
