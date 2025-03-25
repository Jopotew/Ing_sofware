import pymysql
class DatabaseConnection:
    """
    Manages the connection to the MySQL database and provides query execution methods.
    """

    def __init__(self):
        """
        Initializes the database connection parameters.
        """
        self.connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='Jopotew22!!',
        database='macetoide',
        port=3306
        )

        self.cursor = self.connection.cursor() 
      

    def execute_query(self, query):
        """
        Executes the given SQL query and returns the result.
        """
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except pymysql.connect.Error as error:
            print(f"Failed to execute query: {error}")
            return None

    def close(self):
        """
        Closes the database connection and cursor.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Database connection closed.")


    def create_user(self, name, surname, username, mail, password):
        """
        Calls the pymysql FUNCTION 'create_user' and captures the return value.
        """
        
        if not self.cursor:
            print("❌ No database connection.")
            return None

        try:
            query = "SELECT create_user(%s, %s, %s, %s, %s)"
            values = (name, surname, username, mail, password)
            self.cursor.execute(query, values)

            result = self.cursor.fetchone()

            if result and result[0] == 1:
                print("✅ User created successfully via SQL FUNCTION.")
            else:
                print("❌ Failed to create user via SQL FUNCTION.")

            self.connection.commit()
            return result[0]

        except pymysql.connect.Error as error:
            print(f"❌ Failed to execute create_user function: {error}")
            return None




# Example usage
if __name__ == "__main__":
    db= DatabaseConnection()
    result = db.create_user("juan", "maletti", "juancito", "juan@hot.com", "1234")
    print(result)
