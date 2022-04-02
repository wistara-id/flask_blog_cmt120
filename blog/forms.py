# The code for forms.py
#
# This code was adapted from Cardiff University Gitlab Repository by Natasha Edwards 18-11-2021
# accessed 21-01-2022
# https://git.cardiff.ac.uk/scmne/flask-labs/
#
# The adapted code is customized to cater the blog website assessment specification
#
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, SelectField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Regexp, EqualTo, Email
from blog.models import User

# Use of flask_wtf and wtforms to build the blog website
#
# This code was built using FlaskWTF and WTForms documentation by WTForms [No Date]
# accessed 21-01-2022
# https://wtforms.readthedocs.io/en/3.0.x/
# https://flask-wtf.readthedocs.io/en/1.0.x/
#
# The adapted code is customized to cater the blog website assessment specification
#
class RegistrationForm(FlaskForm):
    first_name_new = StringField('First Name', validators=[DataRequired(),\
                        Regexp('^[a-zA-Z0-9]{1,20}$',message='Your first name should be between 1 \
                            and 20 characters long, and can only contain alphanumeric characters.')], \
                    render_kw={'placeholder': 'First Name'})
    email_new = EmailField('Email Address', validators=[DataRequired(), \
                    Email(message='Invalid email. Please check.')], render_kw={'placeholder': 'Email Address'})
    password_new = PasswordField('Password',validators=[DataRequired(),\
                        Regexp('^[a-zA-Z0-9]{1,20}$',message='Your password contain invalid characters. It should be between 1 \
                            and 20 characters long, and can only contain alphanumeric characters.')], \
                    render_kw={'placeholder': 'Password'})
    password_confirm = PasswordField('Repeat Password',validators=[DataRequired(),\
        EqualTo('password_new', message='Password do not match. Please try again.')],\
            render_kw={'placeholder': 'Repeat Password'})
    submit = SubmitField('Register')

    def validate_email_new(self, email_new):
        email_username = User.query.filter_by(email=email_new.data).first()
        if email_username is not None:
            raise ValidationError('Email already registered. Please choose a different one.')

class LoginForm(FlaskForm):
    username_email = EmailField('Email Address',validators=[DataRequired()], render_kw={'placeholder': 'Email Address'})
    password = PasswordField('Password',validators=[DataRequired()], render_kw={'placeholder': 'Password'})
    submit = SubmitField('Login')

class SortForm(FlaskForm):
    sort_option = SelectField(u'Sort Post by date', choices=[('date_desc', 'Newest Post'), ('date_asc', 'Oldest Post')])

class CommentForm(FlaskForm):
    comment = TextAreaField('Leave a comment here...', validators=[DataRequired()], \
                            render_kw={'placeholder': 'Leave a comment here...'})
    submit = SubmitField('Post Comment')

class RatingForm(FlaskForm):
    rating_option = SelectField(u'Choose a rate:', choices=[('5', '5 - Excellent'),
                                                            ('4', '4 - Good'),
                                                            ('3', '3 - Average'),
                                                            ('2', '2 - Poor'),
                                                            ('1', '1 - Very Poor')])
    submit = SubmitField('Rate Post')

