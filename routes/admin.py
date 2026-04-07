from flask import Blueprint,render_template,request,session,redirect,url_for,flash,current_app
from werkzeug.security import generate_password_hash,check_password_hash
from database import db, User,Post,Profile
from .createPost import Post
import os 
admin = Blueprint("admin",__name__)

@admin.route("/view")
def view_users():
    return render_template("View.html",values=User.query.all(),posts=Post.query.all(),profiles=Profile.query.all())


@admin.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@admin.route("/delete_user/<int:user_id>")
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        # Delete all user's posts and images
        posts = Post.query.filter_by(user_id=user_id).all()
        for post in posts:
            filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], 
                                   post.image_path.replace("uploads/", ""))
            if os.path.exists(filepath):
                os.remove(filepath)
            db.session.delete(post)
        
        db.session.delete(user)
        db.session.commit()
    
    return redirect(url_for("admin.view_users"))  # ✅ CHANGE HERE

@admin.route("/delete_post/<int:post_id>")
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post:
        filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], 
                               post.image_path.replace("uploads/", ""))
        if os.path.exists(filepath):
            os.remove(filepath)
        
        db.session.delete(post)
        db.session.commit()
    
    return redirect(url_for("admin.view_users")) 

@admin.route("/delete_changed/<int:user_id>")
def delete_changed(user_id):
    changed = Profile.query.get(user_id)
    if changed:
        if changed.image_path: 
            filepath = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                changed.image_path.replace("uploads/", "")
            )
            if os.path.exists(filepath):
                os.remove(filepath)

        db.session.delete(changed)
        db.session.commit()

    return redirect(url_for("admin.view_users"))