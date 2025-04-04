import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "..")
sys.path.append(src_path)
from database.database import database as db


class Repository:

    def __init__(self):
        self.db = db
        self.table: str = None
        self.id_counter = 0


    def save(self, entity):
        db.create_record(entity, self.table)
        

    def remove(self, entity):
    
        #recibe un dict la bd con tabla: etc
        db.delete_record(entity, self.table)

    def get_all(self):
        return db.get_all(self.table)
    
    def get_by_id(self, id):

        i_dict = db.get_by_id(self.table, id)
        return i_dict
        
        
    

    