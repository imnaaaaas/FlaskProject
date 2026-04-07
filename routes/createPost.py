from flask import Blueprint, render_template, request, session, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from database import db, Post
import os
import time

create = Blueprint("create", __name__)

@create.route("/create", methods=["GET","POST"])
def createPost():
    # ✅ DEBUG: Print session
    print("=" * 50)
    print("SESSION:", dict(session))
    print("=" * 50)
    
    if request.method == "POST":
        user_id = session.get("user_id")
        print(f"User ID from session: {user_id}")
        
        if not user_id:
            print("❌ NO USER_ID - Redirecting to login")
            flash("Please login first", "error")
            return redirect(url_for("auth.login"))
        
        # Get form data
        file = request.files.get("image")
        caption = request.form.get("caption")
        
        print(f"File: {file}")
        print(f"Caption: {caption}")
        
        # Validate file
        if not file or file.filename == "":
            flash("No file uploaded", "error")
            return redirect(url_for("create.createPost"))
        
        # Save file
        filename = str(int(time.time())) + "_" + secure_filename(file.filename)
        filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        
        print(f"Saving to: {filepath}")
        
        # Create uploads folder if missing
        os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)
        
        file.save(filepath)
        print("✅ File saved")
        
        # Save to database
        new_post = Post(
            user_id=user_id,
            image_path="uploads/" + filename,
            caption=caption
        )
        db.session.add(new_post)
        db.session.commit()
        
        print("✅ Post saved to database")
        flash("Post created successfully!", "success")
        
        return redirect(url_for("profile.goto"))
    
    # GET request - show form
    return render_template("CreatePost.html")



