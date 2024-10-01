# forms.py
import email
from flask_wtf import FlaskForm
from wtforms.fields import BooleanField, SelectField, StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, ValidationError, url
from .models import User
class AddNoteForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    content = TextAreaField('content', validators=[DataRequired()] )

class LoginForm(FlaskForm):
    email = StringField('your email: ', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField("keep me logged in")
    submit = SubmitField()

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(3,80)])
    email = StringField('Your Email:', validators=[DataRequired(), Length(1,120), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message = 'Password must match')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username_field):
        user = User.query.filter_by(username=username_field.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email_field):
        user = User.query.filter_by(email=email_field.data).first()
        if user:
            raise ValidationError('That email is already registered. Please use a different one.')
