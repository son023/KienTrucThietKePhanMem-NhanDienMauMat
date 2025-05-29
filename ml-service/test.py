import psycopg2
import psycopg2.extras
def get_connection():
    """
    Get a connection to the database.
    Automatically handles exceptions and raises if connection fails.
    """
    try:
        connection = psycopg2.connect(
            host="localhost",
            port=5432,
            dbname="eye_recognition_db",
            user="postgres",
            password="123456"
        )
        return connection
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        raise

# Usage example:
if __name__ == "__main__":
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1;")  # Example query
                result = cursor.fetchone()
                print(f"Query result: {result}")
    except Exception as e:
        print(f"Error during database operation: {e}")