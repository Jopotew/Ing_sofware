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

    def save(self, entity: dict): #agregar exception a si falla
        return db.save(entity, self.table)

    def delete(self, id):
        return db.delete(id, self.table)

    def get_all(self):
        objs: list = []
        results = db.get_all(self.table)
        for i in results:
            objs.append(self.create_obj(i))
        return objs

    def get_by_id(self, id):
        i_dict = db.get_by_id(self.table, id)
        obj = self.create_obj(i_dict)
        return obj

    def create_obj(self, data: dict):
        pass
