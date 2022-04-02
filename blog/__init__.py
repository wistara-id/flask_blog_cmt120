# Code for __init__.py
#
# This code was adapted from Cardiff University Gitlab Repository by Natasha Edwards 18-11-2021
# accessed 21-01-2022
# https://git.cardiff.ac.uk/scmne/flask-labs/
#
# The adapted code is customized to cater the blog website assessment specification
#
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f7550c31ece7e57c36d32e1b154f9c25a8638af90a859547'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c1986741:Allthebest123!#@csmysql.cs.cf.ac.uk:3306/c1986741_blog'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from blog import routes