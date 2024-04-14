from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms import validators

class LoginForm(FlaskForm):
    username = StringField()
    password = PasswordField()
    submit = SubmitField('Logar')

class RegisterForm(FlaskForm):
    name = StringField('Full name', [validators.DataRequired()])
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    password2 = PasswordField('Password2', [validators.DataRequired()])
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    submit = SubmitField('Register')