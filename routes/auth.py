from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, User,Profile

auth = Blueprint("auth", __name__)
@auth.route("/register", methods=["GET", "POST"])
def register():
    
    if request.method == "POST":
        fullname = request.form["fullname"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirmPassword = request.form["confirmPassword"]

        if password != confirmPassword:
            return "Passwords do not match!"

        hashed_password = generate_password_hash(password)
        found_user = User.query.filter_by(email=email).first()

        if found_user:
            return "Email already exists! Please choose another."
        else:
            new_user = User(fullname=fullname, username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.flush() 

            new_profile = Profile(user_id=new_user.id)
            db.session.add(new_profile)
            db.session.commit()

            session.permanent = False  
            session["user_id"] = new_user.id
            session["fullname"] = fullname
            session["username"] = username
            session["email"] = email

            return redirect(url_for("auth.login"))

    return render_template("Register.html")



@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        found_user = User.query.filter_by(email=email).first()
        print(found_user)  
        if found_user:
            if check_password_hash(found_user.password, password):
                session.permanent = False  
                session["user_id"] = found_user.id 
                session["fullname"] = found_user.fullname
                session["username"] = found_user.username
                session["email"] = found_user.email
                return redirect(url_for("profile.goto"))
            else:
                flash("Incorrect password", "error")
                return redirect(url_for("auth.login"))
        else:
            flash("User doesn't exist! Please register first!", "error")
            return redirect(url_for("auth.login"))

    return render_template("Login.html")




@auth.route("/", methods=["GET", "POST"])
def home():
   return render_template("Welcome.html")



