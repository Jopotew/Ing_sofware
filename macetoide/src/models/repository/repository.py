from macetoide.src.models.database.database import database as db


class Repository:

    def __init__(self):
        self.db = db
        self.table: str = None
        self.id_counter = 0


    def save(self, entity, table):
        self.db.create_record(entity, table)
        

    def remove(self, entity):
        print
        #recibe un dict la bd con tabla: etc
        self.db.delete_record(entity)

    def get_all(self):
        return self.database
    
    def get_by_id(self, table, id):
        
    

    