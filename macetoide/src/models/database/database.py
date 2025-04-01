import pymysql


class DatabaseConnection:

    def __init__(self):
        self.connection = pymysql.connect(
            host="192.168.0.21",
            user="jp",
            password="Juanpi22!",
            database="macetoide",
            port=3306,
        )

        self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except pymysql.connect.Error as error:
            print(f"Failed to execute query: {error}")
            return None

    def close(self):

        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

    def create_record(self, data, table):

        try:
            function_map = {
                "pot": "create_pot",
                "plant": "create_plant",
                "log": "create_log",
                "user": "create_user",
            }

            if table not in function_map:
                print("Invalid table name.")
                return 0

            sql_function = function_map[table]

            params = [v for k, v in data.items() if k != "table"]
            placeholders = ", ".join(["%s"] * len(params))

            query = f"SELECT {sql_function}({placeholders})"
            self.cursor.execute(query, params)
            result = self.cursor.fetchone()

            if result and result[0] == 1:
                print(f"{table} record created successfully.")
            else:
                print(f"Failed to create {table} record.")

            self.connection.commit()
            return result[0]

        except pymysql.MySQLError as error:
            print(f"Error executing create function for {table}: {error}")
            return 0

    def delete_record(self, data, table):
        try:
            function_map = {
                "pot": "delete_pot",
                "plant": "delete_plant",
                "log": "delete_log",
                "user": "delete_user",
            }

            if table not in function_map:
                print("Invalid table name.")
                return 0

            sql_function = function_map[table]

            record_id = data.get("id")
            if record_id is None:
                print("Missing 'id' parameter.")
                return 0

            query = f"SELECT {sql_function}(%s)"
            self.cursor.execute(query, (record_id,))
            result = self.cursor.fetchone()

            if result and result[0] == 1:
                print(f"{table} record deleted successfully.")
            else:
                print(f"Failed to delete {table} record or record not found.")

            self.connection.commit()
            return result[0]

        except pymysql.MySQLError as error:
            print(f"Error executing delete function for {table}: {error}")
            return 0

    def update_pot_last_checked(self, pot_id, last_checked_time):
        try:
            query = "SELECT update_pot_last_checked(%s, %s)"
            self.cursor.execute(query, (pot_id, last_checked_time))
            result = self.cursor.fetchone()

            if result and result[0] == 1:
                print("last_checked updated successfully.")
            else:
                print("Failed to update last_checked or no matching pot.")

            self.connection.commit()
            return result[0]

        except pymysql.MySQLError as error:
            print(f"Error executing function: {error}")
            return 0

    def update_pot_analysis_time(self, pot_id, analysis_time):
        try:
            self.cursor.callproc("update_pot_analysis_time", (pot_id, analysis_time))
            self.connection.commit()
            print("analysis_time updated successfully.")
            return 1
        except pymysql.MySQLError as error:
            print(f"Error executing update_pot_analysis_time: {error}")
            return 0

    def update_pot_id_plant(self, pot_id, new_plant_id):
        try:
            query = "SELECT update_pot_id_plant(%s, %s)"
            self.cursor.execute(query, (pot_id, new_plant_id))
            result = self.cursor.fetchone()

            if result and result[0] == 1:
                print("id_plant updated successfully in pot.")
            else:
                print("Failed to update id_plant or pot not found.")

            self.connection.commit()
            return result[0]

        except pymysql.MySQLError as error:
            print(f"Error executing update_pot_id_plant: {error}")
            return 0

    def get_all(self, table):
        try:
            function_map = {
                "plant": "get_all_plants",
                "user": "get_all_users",
                "pot": "get_all_pots",
                "log": "get_all_logs",
            }

            if table not in function_map:
                print("Invalid table name.")
                return 0

            sql_function = function_map[table]
            query = f"SELECT {sql_function}()"
            self.cursor.execute(query)
            result = self.cursor.fetchone()

            print(f"Total {table} records: {result[0]}")
            return result[0]

        except pymysql.MySQLError as error:
            print(f"Error executing get_all for {table}: {error}")
            return 0

    def get_by_id(self, table, id):
        try:
            function_map = {
                "plant": "get_plant_by_id",
                "user": "get_user_by_id",
                "pot": "get_pot_by_id",
                "log": "get_log_by_id",
            }

            if table not in function_map:
                print("Invalid table name.")
                return 0

            sql_function = function_map[table]
            query = f"SELECT {sql_function}(%s)"
            self.cursor.execute(query, (id,))
            result = self.cursor.fetchone()

            if result and result[0] > 0:
                print(f"{table} with ID {id} exists.")
            else:
                print(f"{table} with ID {id} does not exist.")

            return result[0]

        except pymysql.MySQLError as error:
            print(f"Error executing get_by_id for {table}: {error}")
            return 0

    def get_by_username(self, username):
        try: 
            self.cursor.callproc("get_by_username", [username])
            result = result = self.cursor.fetchall()
            return result

        except pymysql.MySQLError as error:
            print(f"Error executing get_user_pots: {error}")
            return []

    def get_user_pots(self, user_id):
        try:
            self.cursor.callproc("get_user_pots", [user_id])
            result = self.cursor.fetchall()
            return result

        except pymysql.MySQLError as error:
            print(f"Error executing get_user_pots: {error}")
            return []

    def get_all_logs_by_pot(self, pot_id):
        try:
            self.cursor.callproc("get_logs_by_pot", [pot_id])
            logs = self.cursor.fetchall()
            return logs
        except pymysql.MySQLError as error:
            print(f"Error executing get_logs_by_pot: {error}")
            return []

    def get_all_plants_by_user(self, user_id):
        try:
            self.cursor.callproc("get_plants_by_user", [user_id])
            plants = self.cursor.fetchall()
            return plants
        except pymysql.MySQLError as error:
            print(f"Error executing get_plants_by_user: {error}")
            return []

    def get_all_logs_by_plant(self, plant_id):
        try:
            self.cursor.callproc("get_logs_by_plant", [plant_id])
            logs = self.cursor.fetchall()
            return logs
        except pymysql.MySQLError as error:
            print(f"Error executing get_logs_by_plant: {error}")
            return []

    def get_all_logs_by_user(self, user_id):
        try:
            self.cursor.callproc("get_logs_by_user", [user_id])
            logs = self.cursor.fetchall()
            return logs
        except pymysql.MySQLError as error:
            print(f"Error executing get_logs_by_user: {error}")
            return []

    def get_last_logs_by_user(self, user_id):
        try:
            self.cursor.callproc("get_last_logs_by_user", [user_id])
            logs = self.cursor.fetchall()
            return logs
        except pymysql.MySQLError as error:
            print(f"Error executing get_last_logs_by_user: {error}")
            return []

    def get_last_log_by_pot(self, pot_id):
        try:
            self.cursor.callproc("get_last_log_by_pot", [pot_id])
            log = self.cursor.fetchone()
            return log
        except pymysql.MySQLError as error:
            print(f"Error executing get_last_log_by_pot: {error}")
            return None





class FakeDatabase():

    def __init__(self):
        

        self.users = [
        {"id": 1, "username": "juan", "password": "", "mail": "juan@123.com"},
        {"id": 2, "username": "maria", "password": "", "mail": "maria@correo.com"},
        {"id": 3, "username": "luis", "password": "", "mail": "luis@example.com"},
        {"id": 4, "username": "ana", "password": "", "mail": "ana@dominio.com"},
        {"id": 5, "username": "pedro", "password": "", "mail": "pedro@mail.com"},
        ]

        self.pots = [
            {
                "id": 1,
                "name": "Maceta de juan #1",
                "plant_id": 1,
                "analysis_time": "08:00",
                "last_checked": "09:00",
                "user_id": 1,
            },
            {
                "id": 2,
                "name": "Maceta de ana #2",
                "plant_id": 2,
                "analysis_time": "08:10",
                "last_checked": "09:10",
                "user_id": 4,
            },
            {
                "id": 3,
                "name": "Maceta de luis #3",
                "plant_id": 3,
                "analysis_time": "08:20",
                "last_checked": "09:20",
                "user_id": 3,
            },
            {
                "id": 4,
                "name": "Maceta de maria #4",
                "plant_id": 4,
                "analysis_time": "08:30",
                "last_checked": "09:30",
                "user_id": 2,
            },
            {
                "id": 5,
                "name": "Maceta de pedro #5",
                "plant_id": 5,
                "analysis_time": "08:40",
                "last_checked": "09:40",
                "user_id": 5,
            },
        ]

        self.plants = [
            {
                "id": 1,
                "name": "Aloe Vera",
                "species": "Aloe barbadensis miller",
                "description": "",
            },
            {"id": 2, "name": "Menta", "species": "Mentha spicata", "description": ""},
            {
                "id": 3,
                "name": "Lavanda",
                "species": "Lavandula angustifolia",
                "description": "",
            },
            {"id": 4, "name": "Romero", "species": "Salvia rosmarinus", "description": ""},
            {"id": 5, "name": "Cilantro", "species": "Coriandrum sativum", "description": ""},
        ]

        self.logs = [
            {
                "id": 1,
                "pot_id": 1,
                "plant_id": 1,
                "temperature": 22.5,
                "soil_humidity": 40.2,
                "air_humidity": 55.1,
                "image_path": "images/pot1_20250330_0800.jpg",
                "expert_advice": "La humedad del suelo es buena. No es necesario regar.",
                "timestamp": "2025-03-30 08:00:00",
            },
            {
                "id": 2,
                "pot_id": 1,
                "plant_id": 1,
                "temperature": 24.1,
                "soil_humidity": 28.6,
                "air_humidity": 60.3,
                "image_path": "images/pot2_20250330_0810.jpg",
                "expert_advice": "El suelo está un poco seco. Riego ligero recomendado.",
                "timestamp": "2025-03-30 08:10:00",
            },
            {
                "id": 3,
                "pot_id": 1,
                "plant_id": 1,
                "temperature": 23.8,
                "soil_humidity": 15.0,
                "air_humidity": 50.0,
                "image_path": "images/pot3_20250330_0820.jpg",
                "expert_advice": "El nivel de humedad es crítico. Regar inmediatamente.",
                "timestamp": "2025-03-30 08:20:00",
            },
            {
                "id": 4,
                "pot_id": 4,
                "plant_id": 4,
                "temperature": 21.0,
                "soil_humidity": 45.3,
                "air_humidity": 48.9,
                "image_path": "images/pot4_20250330_0830.jpg",
                "expert_advice": "Todo en orden. Buena temperatura y humedad.",
                "timestamp": "2025-03-30 08:30:00",
            },
            {
                "id": 5,
                "pot_id": 5,
                "plant_id": 5,
                "temperature": 25.0,
                "soil_humidity": 10.5,
                "air_humidity": 42.0,
                "image_path": "images/pot5_20250330_0840.jpg",
                "expert_advice": "Riego urgente requerido. Condiciones desfavorables.",
                "timestamp": "2025-03-30 08:40:00",
            },
        ]


    def update_user(self, user_id: int, field: str, old_value: str, new_value: str) -> bool:
        if field not in ["username", "password", "mail"]:
            return False
      
        for user in self.users:
            if user["id"] == user_id:
                if user.get(field) != old_value:
                    return False
                user[field] = new_value
                return True

        return False
  

    def get_by_username(self, username):
        for user in self.users:
            if user["username"] == username:
                return user
        return None


    def get_by_id(self, table, id):
        if table == "user":
            for user in self.users:
                if user["id"] == id:
                    return user
            return None
        elif table == "log":
            for log in self.logs:
                if log["id"] == id:
                    return log
            return None
        elif table == "plants":
            for plant in self.plants:
                if plant["id"] == id:
                    return plant
            return None
        elif table == "pots":
            for pot in self.pots:
                if pot["id"] == id:
                    return pot
            return None
        else:
            return None

    def get_pots(self, user_id):
        u_pots: list = []
        for pot in self.pots:
            if pot["user_id"] == user_id:
                u_pots.append(pot)
        return u_pots


    def save(self, table, data_dict):
        
        if table == "log":
            target_list = self.logs
        elif table == "pots":
            target_list = self.pots
        elif table == "plants":
            target_list = self.plants
        elif table == "user":
            target_list = self.users
        else:
            return False  

        for i, existing in enumerate(target_list):
            if existing["id"] == data_dict["id"]:
                target_list[i] = data_dict
                return True

        target_list.append(data_dict)
        return True


    def get_last_log(self, pot_id):
        logs = []
        for log in self.logs:
            if log["pot_id"] == pot_id:
                logs.append(log)
        if len(logs)==0:
            return []
        else:
            return logs[-1]
    
    def get_all_logs(self, pot_id):
        logs = []
        for log in self.logs:
            if log["pot_id"] == pot_id:
                logs.append(log)
        return logs


# falta user (validaciones)
database = FakeDatabase()
