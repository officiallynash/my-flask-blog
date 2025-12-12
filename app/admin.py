from flask import Blueprint, render_template, flash, get_flashed_messages
from flask import redirect, url_for, request, session
from config import DB_Process, slugify
from datetime import datetime

# Database Processing and Slugify
db = DB_Process()

# Blueprint
adm = Blueprint('admin', __name__, url_prefix='/')

# Admin Area
@adm.route('/admin')
def admin():
    if 'username' not in session :
        return redirect(url_for("public.login"))
    else:
        return render_template("admin.html")

# Logout
@adm.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for("public.index"))

# Writing a post
@adm.route('/write', methods=["GET","POST"])
def write_blog():
    if 'username' not in session :
        return redirect(url_for("public.login"))
    else :
        if request.method == "GET":
            post = db.show_all()
            categories = db.show_categories()
            return render_template('write_blog.html', post=post, categories=categories)
        else :
            title = request.form.get('title')
            content = request.form.get('content')
            date = datetime.now()
            date = date.strftime('%Y-%m-%d %H:%M:%S')
            cat_id = request.form.get('cat_id')
            slug = slugify(title)
            
            insert = db.insert_data(title, slug, date, content, cat_id)

            if insert == 'SUCCESS' :
                flash(f"The post has been successfully published!")
                return redirect(url_for("admin.write_blog"))
            else :
                flash(f"The post failed to publish")
                return redirect(url_for("admin.write_blog"))



# delete post (Admin Mode)
@adm.route('/delete/<int:id>')
def delete_post(id):

    if 'username' not in session :
        return redirect(url_for("public.index"))
    else :
        hapus = db.delete_post(id)

        if hapus == 'SUCCESS' :
            flash(f"The post has been successfully deleted!")
            return redirect(url_for("admin.write_blog"))
        else :
            flash(f"The post failed to delete!")
            return redirect(url_for("admin.write_blog"))

# edit post (Admin Mode)
@adm.route('/edit/<int:id>', methods=["GET","POST"])
def edit_post(id):
    
    if 'username' in session:
        
        if request.method == "GET":
            post = db.edit_post(id)
            categories = db.show_categories()

            return render_template('edit_post.html', post=post, categories=categories)
        
        else :
            title = request.form.get('title')
            content = request.form.get('content')
            cat_id = request.form.get('cat_id')

            edit = db.update_post(id, title, content, cat_id)
            if edit == 'SUCCESS' :
                flash(f"The post has been successfully edited!")
                return redirect(url_for("admin.write_blog"))
            else :
                flash(f"The post failed to edit!")
                return redirect(url_for("admin.write_blog"))

    else :
        return redirect(url_for("public.login"))

# show category at admin panel
@adm.route('/categories', methods=["GET","POST"])
def categories():
    if 'username' in session :
        if request.method == "GET":
            data = db.show_categories()
            return render_template('show_categories.html', data=data)


        else:
            cat_name = request.form.get('cat_name')
            slug = slugify(cat_name)
            data = db.create_categories(cat_name, slug)
            if data == 'SUCCESS' :
                flash(f"Created successfully!")
                return redirect(url_for("admin.categories"))
            else :
                flash(f"Failed!")
                return redirect(url_for("admin.categories"))
    else :
        return redirect(url_for("public.index"))
