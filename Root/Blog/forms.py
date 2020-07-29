from flask_wtf import FlaskForm
#file upload
from flask_wtf.file import FileField, FileRequired
from werkzeug.datastructures import CombinedMultiDict
#
from wtforms import StringField, PasswordField, HiddenField, SubmitField, BooleanField, TextAreaField,BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.widgets import TextArea
from Blog.model import User

import re

class Sign_Up_Form(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8)])
    check_password = PasswordField('Confirm password', validators=[DataRequired(),EqualTo('Password')])
    submit = SubmitField('Sign up')

    file = FileField('Thumbnail upload')
    
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
    username = StringField('Username', validators=[DataRequired(),Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8)])
    remember = BooleanField('Stay logged in?')
    submit = SubmitField('Login')

class New_Post_Form(FlaskForm):
    title = StringField('Title', validators=[DataRequired(),Length(min=4, max=25)])
    description = TextAreaField('Description', widget=TextArea(),validators=[DataRequired()])
    private = BooleanField('Would you like to make your post private?')
    submit = SubmitField('Post')
    image = FileField('Thumbnail upload')
    file = FileField('File upload')


class Edit_Profile_Form(FlaskForm):
    username = HiddenField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    about = TextAreaField('About')
    pinned_uploads = StringField('Pinned')
    submit = SubmitField('Post')
    user_photo = FileField("Thumbnail upload")
    file = FileField('File upload')


