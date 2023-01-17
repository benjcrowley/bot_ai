"""Models for the app"""
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    """User model"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    premium = db.Column(db.Boolean, nullable=False, default=False)

    # ratings = a list of ratings objects

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Script(db.Model):
    """Script model"""

    __tablename__ = "scripts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_file = db.Column(db.String(), nullable=False, default="default.jpg")
    file_name = db.Column(db.String(), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, title, description, price, image_file, file_name):
        self.title = title
        self.description = description
        self.price = price
        self.image_file = image_file
        self.file_name = file_name

    # ratings = a list of rating objects

    def __repr__(self):
        return f"Script('{self.title}', '{self.description}', '{self.price}', '{self.image_file}', '{self.date_posted}')"


class Reviews(db.Model):
    """Reviews model"""

    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    script_id = db.Column(db.Integer, db.ForeignKey("scripts.id"), nullable=False)

    user = db.relationship("User", backref=db.backref("reviews", lazy=True))
    script = db.relationship("Script", backref=db.backref("reviews", lazy=True))

    def __repr__(self):
        return f"Reviews('{self.rating}', '{self.review}', '{self.date_posted}')"


def connect_to_db(flask_app, echo=True):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    db.app = flask_app
    db.init_app(flask_app)


# connect to the database
if __name__ == "__main__":
    from server import app

    connect_to_db(app, echo=False)
    print("Connected to DB.")
