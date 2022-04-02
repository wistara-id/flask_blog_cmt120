# Code for routes.py
#
# This code was adapted from Cardiff University Gitlab Repository by Natasha Edwards 18-11-2021
# accessed 21-01-2022
# https://git.cardiff.ac.uk/scmne/flask-labs/
#
# The adapted code is customized to cater the blog website assessment specification
#

from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from blog import app, db
from blog.models import Rating, User, Post, Comment
from blog.forms import CommentForm, RegistrationForm, LoginForm, SortForm, RatingForm
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import desc, asc
from datetime import datetime

# Use of SQLAlchemy to build the blog website
#
# This code was built using SQLAlchemy documentation by SQLAlchemy authors and contributors. [No Date]
# accessed 21-01-2022
# https://docs.sqlalchemy.org/en/14/
#
# The adapted code is customized to cater the blog website assessment specification
#

# Use of Flask-Login to build the blog website
#
# This code was built using Flask-Login documentation by Max Countryman and Flask-Login contributors. [No Date]
# accessed 21-01-2022
# https://flask-login.readthedocs.io/en/latest/
#
# The adapted code is customized to cater the blog website assessment specification
#

@app.route('/')
def root():
    return redirect(url_for('home'))

@app.route("/home",methods=['GET','POST'])
def home():
    form = SortForm()
    if form.sort_option.data == 'date_asc':
        posts=Post.query.order_by(asc(Post.date)).all()
    else:
        posts=Post.query.order_by(desc(Post.date)).all()
    return render_template('home.html',posts=posts, form=form)

@app.route("/post/<int:post_id>",methods=['GET','POST'])
def post(post_id):
    form_comment = CommentForm()
    form_rating =RatingForm()
    if current_user.is_authenticated:
        if request.method == 'POST':
            if 'submit_comment' in request.form:
                comment = Comment(content=form_comment.comment.data,
                            date=datetime.utcnow(),
                            post_id=post_id,
                            reg_user_id=current_user.id)
                db.session.add(comment)
                db.session.commit()
                flash('Comment successful.', 'flash_success')
                return redirect(url_for('post',post_id=post_id))
            elif 'submit_rating' in request.form:
                check_rating = Rating.query.filter_by(reg_user_id=current_user.id,post_id=post_id).first()
                if check_rating is None:
                    rating = Rating(rating_scale=form_rating.rating_option.data,
                                    post_id=post_id,
                                    reg_user_id=current_user.id)
                    db.session.add(rating)
                    db.session.commit()
                    flash('Rating successful.', 'flash_success')
                else:
                    check_rating.rating_scale = form_rating.rating_option.data
                    db.session.commit()
                    flash('Rating updated.', 'flash_success')
                return redirect(url_for('post',post_id=post_id))

    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).order_by(desc(Comment.date)).all()
    ratings = Rating.query.filter_by(post_id=post_id).all()
    user_rating = []
    if current_user.is_authenticated:
        user_rating = Rating.query.filter_by(reg_user_id=current_user.id,post_id=post_id).all()

    return render_template('post.html', title=post.title, post=post,form_comment=form_comment,
                           form_rating=form_rating, comments=comments, ratings=ratings,user_rating=user_rating)

@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(firstname=form.first_name_new.data,
                    email=form.email_new.data,
                    password=form.password_new.data)
        db.session.add(user)
        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            flash('Sorry, there is a problem with your registration.', 'register_error')
            db.session.rollback()
        login_user(user)
        flash('Registration successful.', 'flash_success')
        return redirect(url_for('home'))
    return render_template('register.html',title='Register',form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.username_email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash('You\'ve successfully logged in,'+' '+ current_user.firstname +'.', 'flash_success')
            return redirect(url_for('home'))
        flash('Incorrect email or password supplied.','login_error')
    return render_template('login.html',title='Login',form=form)

@app.route("/logout")
@login_required
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    logout_user()
    flash('You have been logged out.', 'flash_success')
    return redirect(url_for('home'))
