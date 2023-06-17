from FlaskApp import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.declarative import declarative_base


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=True)
    email= db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True, cascade='all, delete')


    def __str__(self):
        return self.username


class Post(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    content = db.Column(db.Text, nullable=False)
    privacy = db.Column(db.String(20), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __str__(self):
        return self.title


class Friendship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)



   