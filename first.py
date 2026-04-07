from flask import Flask
from datetime import timedelta
from database import db, User, Post,Profile
from routes.auth import auth  
from routes.profile import profile
from routes.admin import admin
from routes.createPost import create
from routes.editPost import editPost
from routes.guestProfile import guest

app = Flask(__name__)

app.secret_key = "imna2"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=10)
app.config["UPLOAD_FOLDER"] = "static/uploads"

# Initialize and register
db.init_app(app)
app.register_blueprint(auth)
app.register_blueprint(profile)
app.register_blueprint(admin)
app.register_blueprint(create)
app.register_blueprint(editPost)
app.register_blueprint(guest)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
        # Auto-create Profile for existing users who don't have one
        for user in User.query.all():
            if not Profile.query.filter_by(user_id=user.id).first():
                db.session.add(Profile(user_id=user.id))
        db.session.commit()

        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        print("Tables:", inspector.get_table_names())
    app.run(debug=True)