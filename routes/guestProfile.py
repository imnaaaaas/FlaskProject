from flask import Blueprint,render_template,request,session,redirect,url_for,flash,current_app
from werkzeug.utils import secure_filename
from database import db, User, Post,Profile
import os

guest = Blueprint("guest", __name__) 

@guest.route("/guest/<int:user_id>", methods=["GET", "POST"])
def guestProfile(user_id):
    logged_in_user_id = session.get("user_id")  
    
    if not logged_in_user_id:  
        return redirect(url_for("auth.login"))
    
    all_posts = Post.query.filter_by(user_id=user_id).order_by(Post.timestamp.desc()).all()
    user_profile = Profile.query.filter_by(user_id=user_id).first()

    return render_template("GuestProfile.html",
                           all_posts=all_posts,
                           user_profile=user_profile,
                           fullname=user_profile.user.fullname if user_profile else "",
                           profile_user_id=user_id,              # ← add this
                           current_user_id=logged_in_user_id)    # ← add this