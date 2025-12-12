from config import DB_PATH, slugify, DB_Process
import sqlite3
import bcrypt
from datetime import datetime

ins = DB_Process()

class Install:
    def __init__(self):
        self.db_file = DB_PATH

    def db(self):
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row 
        return conn
    def admin_table(self):
        conn = self.db()
        cursor = conn.cursor()

        query = """
        CREATE TABLE IF NOT EXISTS user (
        user_id INTEGER PRIMARY KEY,
        username CHAR NOT NULL,
        password TEXT
        );"""

        cursor.execute(query)
        conn.commit()
        print(f"Table user successfully created!")
        conn.close()
    
    def create_user_data(self):
        conn = self.db()
        cursor = conn.cursor()

        query = """
        INSERT INTO user (username, password) VALUES (?, ?);
        """
        user = input("Username : ")
        pwd = input("Password : ")
        bytes = pwd.encode('utf-8')
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes, salt)

        data = (user, hash)
        cursor.execute(query, data)
        conn.commit()
        print(f"{user} and {pwd} were successfully saved in the Database!")
        conn.close()

    def create_table_post(self):
        conn = self.db()
        cursor = conn.cursor()
        query = """
        CREATE TABLE post (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        slug TEXT NOT NULL,
        date TEXT NOT NULL,
        content TEXT NOT NULL,
        cat_id INTEGER NOT NULL
        );"""
        cursor.execute(query)
        conn.commit()
        print(f"Table post successfully created!")
        conn.close()    


    def categories(self):
        conn = self.db()
        cursor = conn.cursor()
        query = """
        CREATE TABLE categories (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        slug TEXT NOT NULL
        );
        """

        cursor.execute(query)
        conn.commit()

        query2 = """
        INSERT INTO categories (name, slug) VALUES (?, ?);
        """
        data = "Others"
        slug = slugify(data)
        data = (data, slug)
        cursor.execute(query2, data)
        conn.commit()

        print(f"Table categories with default category Others successfully created!")
        conn.close()

    def new_post(self):
        title = "Hello World!"
        content = """
        <p>Hello! This is my first post in this blog. Enjoy!</p>
        """
        cat_id = 1
        slug = slugify(title)
        date = datetime.now()
        date = date.strftime('%Y-%m-%d %H:%M:%S')
        ins.insert_data(title, slug, date, content, cat_id)



app = Install()
print(f"Welcome to Installaion")
print(f"Default Database is database.db were located in the folder db.")
print(f"Create table user.")
app.admin_table()
print(f"Now create a Username and Password for authentication.")
app.create_user_data()
print(f"Create table post.")
app.create_table_post()
app.new_post()
print(f"Create table categories.")
app.categories()
print(f"Setup has been completed. Enjoy!")
exit()