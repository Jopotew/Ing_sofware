import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "..")
sys.path.append(src_path)


from models.entities.pot import Pot
from models.entities.user import User
from models.repository.repository import Repository
from models.database.database import database as db






class FakeRepository(Repository):
    

    def get_by_username(username):
        u = db.get_by_username(username)
        if u is None:
            return None
        pot_list:list = db.get_pots(u["id"])
        pots:list = []
        if len(pot_list) == 0:
            return User(u["id"],u["username"],u["mail"],u["password"], pots)
        for pot in pot_list:
            p = Pot(pot["id"],pot["name"],pot["plant_id"],pot["analysis_time"],pot["user_id"],pot["last_checked"],)
            pots.append(p)
        return User(u["id"],u["username"],u["mail"],u["password"], pots)
            
        
             
        
        
        

    def get_by_id(self, id):
        for user in users:
            if user["id"] == id:
                return User(user["id"], user["username"], user["mail"], user["password"])
        return None 
    
    def get_pot():
        pass

    def get_all_pots():
        pass

    def get_last_log():
        pass

    def get_all_logs():
        pass

instance = FakeRepository








