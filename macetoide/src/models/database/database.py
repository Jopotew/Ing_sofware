import pymysql


class DatabaseConnection:

    def __init__(self):
        self.connection = pymysql.connect(
            host="127.0.0.1",
            user="root",
            password="Jopotew22!!",
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


# falta user (validaciones)
database = DatabaseConnection()
