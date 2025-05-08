import psycopg2

def get_connection():
    """Get a connection to the database"""
    try:
        connection = psycopg2.connect(
            host="localhost",
            port=5432,
            dbname="eye_recognition_db",
            user="postgres",
            password="123456"
        )
        return connection
    except Exception as e:
        print(f"Database connection error: {e}")
        raise