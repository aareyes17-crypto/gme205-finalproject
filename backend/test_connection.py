from database import get_connection

def test_database_connection():
    """
    Test the PostgreSQL/PostGIS database connection.
    """

    try:
        # Create connection
        connection = get_connection()

        # Create cursor
        cursor = connection.cursor()

        # Execute a simple SQL query
        cursor.execute("SELECT version();")

        # Fetch result
        result = cursor.fetchone()

        print("\n===================================")
        print("DATABASE CONNECTION SUCCESSFUL")
        print("===================================")

        print("\nPostgreSQL Version:")
        print(result[0])

        # Close resources
        cursor.close()
        connection.close()

        print("\nConnection closed successfully.")

    except Exception as error:

        print("\n===================================")
        print("DATABASE CONNECTION FAILED")
        print("===================================")

        print("\nError:")
        print(error)

if __name__ == "__main__":
    test_database_connection()
