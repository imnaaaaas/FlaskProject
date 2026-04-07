from flask import Blueprint,render_template,request,session,redirect,url_for,flash,current_app
from werkzeug.utils import secure_filename
from database import db, User, Post,Profile
import os
import time
import random

profile = Blueprint("profile", __name__)

@profile.route("/home", methods=["GET", "POST"])
def goto():
    user_id = session.get("user_id")  
    
    if not user_id:  #  ADDED: Redirect if not logged in
        return redirect(url_for("auth.login"))
    
    #  CHANGED: Filter posts by current user only
    posts = Post.query.filter_by(user_id=user_id).order_by(Post.timestamp.desc()).all()
    user_profile = Profile.query.filter_by(user_id=user_id).first() 
    
    #suggestion users
    all_profiles = Profile.query.filter(Profile.user_id != user_id).all()
    suggested_users = random.sample(all_profiles, min(2, len(all_profiles)))

    return render_template("Home.html",
                        fullname=session.get("fullname"),
                        username=session.get("username"),
                        posts=posts,
                        profile=user_profile,
                        suggested_users=suggested_users)



@profile.route("/profilePage", methods=["GET", "POST"])
def profilePage():
    user_id = session.get("user_id") 
      
    if not user_id:  
        return redirect(url_for("auth.login"))
    
    user_profile = Profile.query.filter_by(user_id=user_id).first()
    posts = Post.query.filter_by(user_id=user_id).order_by(Post.timestamp.desc()).all()
    
    return render_template("Profile.html",fullname=session.get("fullname"),
                            username=session.get("username"),
                            posts=posts,
                            profile=user_profile)



