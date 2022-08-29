from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from shop.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), Length(min=2, max=20)])
    
    email = StringField('Email', validators=[
        DataRequired(), Email()])
    
    password = PasswordField('Password', validators=[
        DataRequired()])
    
    confirm_password = PasswordField('Repeat password', validators=[
        DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), Email()])
    
    password = PasswordField('Password', validators=[
        DataRequired()])
    
    remember = BooleanField('Remember me')
    
    submit = SubmitField('Login')
    

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), Length(min=2, max=20)])
    
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    
    email = StringField('Email', validators=[
        DataRequired(), Email()])
    
    submit = SubmitField('Apdate')
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken')




class RequestPasswordForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), Email()])
    
    submit = SubmitField('Requset password reset')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('No account eith this email')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[
        DataRequired()])
    
    confirm_password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Submit password')