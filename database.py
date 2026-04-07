from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Users table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50),  nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

# Posts table
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_path = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)



# Edit profile
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    display_name = db.Column(db.String(50))   
    image_path = db.Column(db.String(200))     
    bio = db.Column(db.String(150))            
    website = db.Column(db.String(200))        
    location = db.Column(db.String(80))         
    is_private = db.Column(db.Boolean, default=False)
    show_activity = db.Column(db.Boolean, default=True)
    allow_mentions = db.Column(db.Boolean, default=True)
    user = db.relationship('User', backref='profile_info')

    
