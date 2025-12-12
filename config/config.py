import os
import sqlite3
import re
import unicodedata

CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
DIR_NAME = os.path.dirname(CONFIG_DIR)
DB_FOLDER = 'db'
DB_FILE = 'database.db'

DB_PATH = os.path.join(DIR_NAME, DB_FOLDER, DB_FILE)

database = DB_PATH


class DB_Connection:
    def __init__(self):
        self.db_name = database

    # function for execute query SELECT
    def query(self, sql, params=None, one=False):
        params = params if params is not None else ()
        try:
            with sqlite3.connect(self.db_name) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(sql, params)
                return cursor.fetchone() if one else cursor.fetchall()

        except sqlite3.Error as e:
            print(f"Database error {e}")
            return None


    # function for execute query like INSERT, UPDATE and DELETE
    def execute(self, sql, params=None):
        params = params if params is not None else ()
        try:
            with sqlite3.connect(self.db_name) as conn:
                conn.row_factory = sqlite3.Row 
                cursor = conn.cursor()
                cursor.execute(sql, params)
                conn.commit()
                return cursor.rowcount

        except sqlite3.Error as e:
            print(f"Database error {e}")
            return None

def slugify(title):
    title = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore').decode('ascii')
    title = title.lower()
    title = re.sub(r'[^a-z0-9]+', '-', title)
    title = title.strip('-')
    return title
