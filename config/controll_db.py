import config.config as cfg
import sqlite3
import bcrypt

database = cfg.DB_Connection()

class DB_Process:
    # Initial for DB Connection
    def __init__(self):
        self.db = database

    # Function for auth system
    def login_validation(self, user, pwd):
        usr = (user, )
        
        query = """
        SELECT * FROM user WHERE username = ?;
        """
        
        data = self.db.query(query, usr, one=True)

        if data:
           pwddata = data['password']

           pwduser = pwd.encode('utf-8')
           cek = bcrypt.checkpw(pwduser, pwddata)

           if cek == True :
              return 'SUCCESS'
           else :
              return 'FAILED'
        
        else :
           return 'NOT_FOUND'


    # function for INSERT article to Database
    def insert_data(self, title, slug, date, content, cat_id):

        data = (title, slug, date, content, cat_id)
        
        query = """
        INSERT INTO post (title, slug, date, content, cat_id) VALUES (?, ?, ?, ?, ?);
        """

        data = self.db.execute(query, data)
        
        if data > 0:
           return 'SUCCESS'
        else :
            return 'FAILED'

    # create new category
    def create_categories(self, name, slug):
        query = """
        INSERT INTO categories (name, slug) VALUES (?, ?);
        """
        name = (name, slug, )
        data = self.db.execute(query, name)

        if data > 0:
            return 'SUCCESS'
        else :
            return 'FAILED'

    # showing all post (Admin Mode)
    def show_all(self):
        query = """
        SELECT * FROM post;"""
        post = self.db.query(query)
        return post

    
    # Showing post with pagination
    def show_post(self, page):

        #pagination logic
        per_page = 5
        offset = (page - 1) * per_page
               
        # show all post data
        query1 = """
        SELECT post.title, post.slug, post.date, post.cat_id,
        categories.name, categories.slug FROM post
        JOIN categories ON categories.id = post.cat_id ORDER BY post.id DESC LIMIT ? OFFSET ?;
        """
        data = (per_page, offset)
        post = self.db.query(query1, data)
        query2 = """
        SELECT COUNT(id) FROM post;"""
        total = self.db.query(query2, one=True)
        total_post = total[0]
        # total pages
        total_pages = ( total_post + per_page - 1 ) // per_page # ceilling

        return post, total_pages

    # Showing post detail
    def show_post_detail(self, slug):
        

        query = """
        SELECT post.title, post.date, post.content, post.cat_id,
        categories.name, categories.slug FROM post 
        JOIN categories ON categories.id = post.cat_id WHERE post.slug = ?;
        """
        slug = (slug, )

        post = self.db.query(query, slug, one=True)

        return post

    # Showing all categories 
    def show_categories(self):
        query = """
        SELECT categories.id, categories.name, categories.slug,
        COUNT(post.cat_id) FROM categories
        LEFT JOIN post ON cat_id = categories.id
        GROUP BY categories.id;
        """
        categories = self.db.query(query)
        return categories

    # show post by categories
    def show_post_by_categories(self, slug):
        query2 = """
        SELECT post.title, post.date, post.slug, categories.name FROM categories
        JOIN post ON post.cat_id = categories.id
        WHERE categories.slug = ? 
        ORDER BY post.id DESC;
        """
        slug = (slug, )
        post = self.db.query(query2, slug)
        query = """
        SELECT * FROM categories WHERE slug = ?;"""
        categories = self.db.query(query, slug, one=True)

        return post, categories

    # Function for Delete post (Admin mode)
    def delete_post(self, id):

        id = (id, )

        query = """
        DELETE FROM post WHERE id = ?;
        """

        data = self.db.execute(query, id)

        if data > 0:
           return 'SUCCESS'
        else :
            return 'FAILED'

    # Function for Edit or Update Post (Admin mode)
    def update_post(self, id, title, content, cat_id):
        
        data = (title, content, cat_id, id)

        query = """
        UPDATE post SET title = ?, content = ?, cat_id = ? WHERE id = ?;
        """

        data = self.db.execute(query, data)

        if data > 0:
           return 'SUCCESS'
        else :
            return 'FAILED'

    # Function to show content for edit content (Admin mode)
    def edit_post(self, id):
        query = """
        SELECT * FROM post WHERE id = ?;
        """
        id = (id, )
        post = self.db.query(query, id, one=True)

        return post