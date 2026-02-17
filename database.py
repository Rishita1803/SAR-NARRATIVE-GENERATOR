import psycopg2
import os
from dotenv import load_dotenv

# 1. Load the hidden credentials from .env
load_dotenv()

# 2. DEFINE the function first
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        return conn
    except Exception as e:
        print(f"Error: Could not connect. Details: {e}")
        return None

# 3. CALL the function at the bottom
# This 'if' statement tells Python: "Only run this if I run this file directly"
if __name__ == "__main__":
    print("Attempting to connect...")
    test_conn = get_db_connection() # This is where the function is called
    
    if test_conn:
        print("Success! The database is connected.")
        test_conn.close()
    else:
        print("Failed. Check if your PostgreSQL app is running.")