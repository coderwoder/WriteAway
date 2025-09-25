from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField

from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from flaskblog.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                         validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=5, max=13)])
    confirm_password = PasswordField('Confirm Password',
                             validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up!')
    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This Username exist, try another one...')
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This Email exist, try another one...')

class LoginForm(FlaskForm):
    email = StringField('Email',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit = SubmitField('Sign In!')

class Updateinfo(FlaskForm):
    username = StringField('Username',
                         validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                      validators=[DataRequired(), Email()])
    profile_img= FileField('Update Profile Image',validators=[FileAllowed(['jpg','png' ])])
    submit = SubmitField('Update')
    def validate_username(self,username):
        if username.data != current_user.username:
            user=User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This Username exist, try another one...')
    def validate_email(self,email):
        if email.data != current_user.email:
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This Email exist, try another one...')


class Request_ResetForm(FlaskForm):
    email = StringField('Email',
                      validators=[DataRequired(), Email()])
    submit = SubmitField('Request Reset Password')
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('No Account with this Email.')

class Pswd_ResetForm(FlaskForm):
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=5, max=13)])
    confirm_password = PasswordField('Confirm Password',
                             validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
