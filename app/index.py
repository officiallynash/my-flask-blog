# Halaman yang mengatur index, login dan logout
from flask import Flask, flash, url_for, redirect, session, render_template
from flask import request, get_flashed_messages, Blueprint
from config import DB_Process 

db = DB_Process()

# Declare blueprint
pub = Blueprint('public', __name__, url_prefix='/')

# Halaman index
@pub.route('/')
@pub.route('/index/<int:integer>')
def index(integer=1):
    post, total_pages = db.show_post(page=integer)
    cat_name = db.show_categories()

    return render_template("index.html", post=post, page=integer, total_pages=total_pages, cat_name=cat_name)

# Validasi login
@pub.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = request.form.get('username')
        password = request.form.get('password')
        cocok = db.login_validation(user, password)

        if cocok == 'SUCCESS' :
            session['username'] = user
            flash(f"Hello, {user.title()}! Welcome Back!.")
            return redirect(url_for("admin.admin"))
        elif cocok == 'FAILED':
            flash("Wrong password!")
            return redirect(url_for("public.login"))
        else :
            flash("Username was not found!")
            return redirect(url_for("public.login"))
    else :
        return render_template("login.html")

# show post detail by slug
@pub.route('/post/<string:slug>')
def blog_detail(slug):
    post = db.show_post_detail(slug)
    return render_template('show_post.html', post=post)

# show post by categories
@pub.route('/categories/<string:slug>')
def show_categories_post(slug):
    post = db.show_post_by_categories(slug)
    post, categories = post
    return render_template("show_post_categories.html", post=post, categories=categories)



