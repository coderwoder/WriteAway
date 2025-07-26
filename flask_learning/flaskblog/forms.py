from flask_login import current_user
from flaskblog.models import User
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import BooleanField, StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError

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

class PostForm(FlaskForm):
    title=StringField('Title',validators=[DataRequired(),Length(min=5,max=200)])
    content=TextAreaField('Content',validators=[DataRequired()])
    submit=SubmitField('Create!')