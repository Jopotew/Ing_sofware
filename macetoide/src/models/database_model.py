import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()
class DatabaseManager:
    def __init__(self, host, user, password, database):
        try:
           
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password= os.getenv("DB_PSW"),
                database="Macetoide"
            )
            self.cursor = self.connection.cursor(dictionary=True)
            print("Connected to database successfully.")
        except Error as e:
            print(f"Error connecting to database: {e}")

    def insert_data(self, table, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, tuple(data.values()))
        self.connection.commit()

    def update_data(self, table, data, condition):
        set_clause = ', '.join([f"{key} = %s" for key in data])
        query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        self.cursor.execute(query, tuple(data.values()))
        self.connection.commit()

    def delete_data(self, table, condition):
        query = f"DELETE FROM {table} WHERE {condition}"
        self.cursor.execute(query)
        self.connection.commit()

    def fetch_data(self, table, columns='*', condition=None):
        if isinstance(columns, list):
            columns = ', '.join(columns)

        query = f"SELECT {columns} FROM {table}"
        if condition:
            query += f" WHERE {condition}"

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_user_table(self):
        return self.fetch_data('user')

    def get_plant_table(self):
        return self.fetch_data('plant')

    def get_analysis_time_table(self):
        return self.fetch_data('analysis_time')

    def get_pot_table(self):
        return self.fetch_data('pot')

    def get_watering_status_table(self):
        return self.fetch_data('watering_status')

    def get_expert_description_table(self):
        return self.fetch_data('expert_description')

    def get_pot_data_table(self):
        return self.fetch_data('pot_data')

    def get_logs_table(self):
        return self.fetch_data('logs')

    def get_pin_config_table(self):
        return self.fetch_data('pin_config')

    def get_irrigation_event_table(self):
        return self.fetch_data('irrigation_event')

    def close_connection(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Database connection closed.")
