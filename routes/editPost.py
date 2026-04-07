from flask import Blueprint,render_template,request,session,redirect,url_for,flash,current_app
from werkzeug.utils import secure_filename
from database import db, User, Post,Profile
import os
import time

editPost = Blueprint("editPost",__name__)

@editPost.route("/editProfile", methods=["GET", "POST"])
def editProfile(): 
    user_id = session.get("user_id")
    if not user_id:
        flash("Please login first", "error")
        return redirect(url_for("profile.goto"))

    user_profile = Profile.query.filter_by(user_id=user_id).first()

    if request.method == "POST":
        display_name = request.form.get("displayName")
        bio = request.form.get("bio")
        website = request.form.get("website")
        location = request.form.get("location")

        file = request.files.get("image")
        image_path = user_profile.image_path if user_profile else None

        if file and file.filename != "":
            filename = str(int(time.time())) + "_" + secure_filename(file.filename)
            filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)
            file.save(filepath)
            image_path = "uploads/" + filename

        if user_profile:
            user_profile.display_name = display_name
            user_profile.bio = bio
            user_profile.website = website
            user_profile.location = location
            if image_path:
                user_profile.image_path = image_path
        else:
            user_profile = Profile(
                user_id=user_id,
                display_name=display_name,
                bio=bio,
                website=website,
                location=location,
                image_path=image_path,
            )
            db.session.add(user_profile)

       
        try:
            db.session.commit()
            flash("Profile saved!", "success")
            return redirect(url_for("profile.goto"))  
        except Exception as e:
            db.session.rollback()
            flash("Something went wrong, changes not saved.", "error")
            print(f"DB ERROR: {e}") 
            return render_template("EditProfile.html", profile=user_profile)
        
    return render_template("EditProfile.html", profile=user_profile)