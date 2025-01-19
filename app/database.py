import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.sql import SQL, Identifier
from dotenv import load_dotenv
import os
import time

load_dotenv(".env")

# while True:
#     try:
#         conn = psycopg2.connect(host=os.getenv('HOST'), database=os.getenv('DATABASE'), user =os.getenv('USER'), password = os.getenv('PASSWORD'),
#                                 port=os.getenv('PORT'), cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database Connection was successful")
#         break
#     except Exception as error:
#         print("Failed to connect to Database")
#         print("Error: ", error)
#         # prevents random and fast connection attempts
#         time.sleep(2)

class DatabaseManager:
    _instance = None
    _conn = None
    _cursor = None

    # new method run initially when a class object is called
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._conn:
            self._connect()
    
    def _connect(self):
        while True:
            try:
                self._conn = psycopg2.connect(
                    host = os.getenv('HOST'),
                    database = os.getenv('DATABASE'),
                    user = os.getenv('USER'),
                    password = os.getenv('PASSWORD'),
                    port = os.getenv('PORT'),
                    cursor_factory=RealDictCursor
                )
                self._cursor = self._conn.cursor()
                print("Database Connection Successful")
                break
            except Exception as error:
                print("Failed to connect to Database")
                print("Error: ", error)
                # prevents random and fast connection attempts
                time.sleep(2)
    
    def get_cursor(self):
        """Returns the cursor object, reconnecting if necessary"""
        if self._conn is None or self._conn.closed:
            self._connect()
        return self._cursor

    def get_connection(self):
        """Returns the connection object, reconnecting if necessary"""
        if self._conn is None or self._conn.closed:
            self._connect()
        return self._conn

    def close(self):
        """Closes the database connection"""
        if self._cursor:
            self._cursor.close()
        if self._conn:
            self._conn.close()
            self._conn = None
            self._cursor = None
