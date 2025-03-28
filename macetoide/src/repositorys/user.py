from macetoide.src.models.entities.log import Log
from macetoide.src.models.entities.pot import Pot
from macetoide.src.models.entities.user import User
from macetoide.src.models.database.database import database as db
from typing import Optional
import bcrypt
from macetoide.src.models.server_credentials.security import verify_password
from macetoide.src.models.repository.repository import Repository


class UserRepository(Repository):

    def __init__(self):
        super().__init__()
        self.table = "user"

    
    def verify_user(self, username: str, password: str) -> User | None:
        """
        Verifica las credenciales de un usuario usando bcrypt.
        """
        users = db.execute_query("SELECT * FROM user")
        for u in users:
            if u["username"] == username and verify_password(password, u["password"]):
                return User(u["id"], u["username"], u["email"])
        return None

    def get_pots(self, user_id: int) -> list[dict]:
        """
        Obtiene todas las macetas de un usuario por su ID.
        """
        pots_dict = db.get_user_pots(user_id)
        user_pots: list[dict] = []

        for pot in pots_dict:
            if pot["id_user"] == user_id:
                new = Pot(pot["id"], pot["name"], pot["id_plant"], pot["analysis_time"], pot["user"], pot["last_checked"])
                user_pots.append(new.get_dto())
        return user_pots

   
    def get_all_logs(self, user):
        user_logs: list[Log] = []
        logs_dict = db.get_all_logs_by_user(user.id)
        for log in logs_dict:
            if log["id_user"] == user.id:
                new = Log(log["id"],log["name"],log["id_plant"],log["analysis_time"],user, log["last_checked"])
                user_logs.append(new)
                
            else: 
                print("Esta maceta no pertenece a este usuario. Acceso Cucatrap")

        return user_logs
    

    def get_last_log(self, user):
        user_logs: list[Log] = []
        last_logs = db.get_last_logs_by_user(user.id)
        for log in last_logs:
            if log["id_user"] == user.id:
                new = Log(log["id"],log["name"],log["id_plant"],log["analysis_time"],user, log["last_checked"])
                user_logs.append(new)
                
            else: 
                print("Esta maceta no pertenece a este usuario. Acceso Cucatrap")

        return user_logs
    

instance = UserRepository()