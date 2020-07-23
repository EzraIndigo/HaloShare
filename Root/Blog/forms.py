from flask_wtf import FlaskForm
#file upload
from flask_wtf.file import FileField, FileRequired
from werkzeug.datastructures import CombinedMultiDict
#
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField,BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.widgets import TextArea
from Blog.model import User

import re

class Sign_Up_Form(FlaskForm):
    username = StringField('username', validators=[DataRequired(),Length(min=4, max=25)])
    email = StringField('email', validators=[DataRequired(),Email()])
    password = PasswordField('password', validators=[DataRequired(),Length(min=8)])
    check_password = PasswordField('confirm password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Oops  :( \nLooks like that username is taken.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Oops  :( \n Looks like someone's using that email already.")
    
    def validate_password(self, password):
        #Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character:
        x = re.search(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password.data)
        if not x:
            raise ValidationError("Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character")

class Login_Form(FlaskForm):
    username = StringField('username', validators=[DataRequired(),Length(min=4, max=25)])
    password = PasswordField('password', validators=[DataRequired(),Length(min=8)])
    remember = BooleanField('Stay logged in?')
    submit = SubmitField('login')

class New_Post_Form(FlaskForm):
    title = StringField('Title', validators=[DataRequired(),Length(min=4, max=25)])
    description = TextAreaField('Description', widget=TextArea(),validators=[DataRequired()])
    private = BooleanField('Would you like to make your post private?')
    submit = SubmitField('Post')
    image = FileField('Thumbnail upload')
    file = FileField('File upload')
