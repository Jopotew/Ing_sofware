


class Repository:

    def __init__(self):
        self.database = []
        self.id_counter = 0


    def save(self, entity):
        self.database.append(entity)
        self.assign_id(entity)

    def remove(self, entity):
        self.database.remove(entity)

    def get_all(self):
        return self.database
    
    def get_by_id(self, id):
        for entity in self.database:
            if entity.id == id:
                return entity
        return None
    

    def assign_id(self, entity):
        entity.id = self.id_counter
        self.id_counter += 1
        return entity.id