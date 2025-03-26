from macetoide.src.models.entities.log import Log
from macetoide.src.models.entities.pot import Pot
from macetoide.src.models.entities.user import User
from macetoide.src.models.database.database import database as db
from typing import Optional

from macetoide.src.models.repository.repository import Repository


class UserRepository(Repository):

    def __init__(self):
        super().__init__()
        self.table = "user"

    
    def get_pots(self, user):
        pots_dict = db.get_user_pots(user.id)
        for pot in pots_dict:
            if pot["id_user"] == user.id:
                new = Pot(pot["id"],pot["name"],pot["id_plant"],pot["analysis_time"],user, pot["last_checked"])
                user.add_pot(new)
                
            else: 
                print("Esta maceta no pertenece a este usuario. Acceso Cucatrap")

        return user.pots
   
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