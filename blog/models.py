# Code for models.py
#
# This code was adapted from Cardiff University Gitlab Repository by Natasha Edwards 18-11-2021
# accessed 21-01-2022
# https://git.cardiff.ac.uk/scmne/flask-labs/
#
# The adapted code is customized to cater the blog website assessment specification
#
from datetime import datetime
from blog import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Use of Flask-Login to build the blog website
#
# This code was built using Flask-Login documentation by Max Countryman and Flask-Login contributors. [No Date]
# accessed 21-01-2022
# https://flask-login.readthedocs.io/en/latest/
#
# The adapted code is customized to cater the blog website assessment specification
#

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(40), nullable=False, default='default.jpg')
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#    comment = db.relationship('Comment', backref='post', lazy=True)
#    rating = db.relationship('Rating', backref='post', lazy=True)

    def __repr__(self):
        return f"Post('{self.date}', '{self.title}', '{self.content}')"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    reg_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    post_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Comment('{self.date}','{self.content}','{self.reg_user_id}','{self.post_id}')"

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating_scale = db.Column(db.Integer, nullable=False)
    reg_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    post_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Rating('{self.rating_scale}','{self.reg_user_id}','{self.post_id}')"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False)
    hashed_password=db.Column(db.String(128))
    post = db.relationship('Post', backref='user', lazy=True)
    comment = db.relationship('Comment', backref='user', lazy=True)
    rating = db.relationship('Rating', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.firstname}', '{self.email}')"

#adated from Grinberg(2014, 2018)
    @property
    def password(self):
        raise AttributeError('Password is not readable.')

    @password.setter
    def password(self,password):
        self.hashed_password=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.hashed_password,password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
