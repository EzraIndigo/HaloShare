from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cd7eacce7ca5ed08d329ad5f52c7c742'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


login_manager = LoginManager(app)
from Blog import routes
from Blog.routes import fkey, fencrypt, fdecrypt
#### JINJA 

app.jinja_env.globals.update(fencrypt=fencrypt)
app.jinja_env.globals.update(fdecrypt=fdecrypt)

##encryption
from cryptography.fernet import Fernet
import base64

def base64_encode(text):
    return base64.urlsafe_b64encode(text)
app.add_template_filter(base64_encode)

def decode(text):
    return text.decode('utf-8')
app.add_template_filter(decode)

def ip_list(input):

    input = str(input)
    ipEnd = len(input)-1
    return(input[2:ipEnd])
app.jinja_env.globals.update(ip_list=ip_list)

##
##
## MEDIA 
##
##
# IMAGE VALIDATION PREREQUISITES------------------------------------------------------------------
IMAGE_ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'} # allowed image file types for post#-----------
def image_allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in IMAGE_ALLOWED_EXTENSIONS
# VIDEO VALIDATION PREREQUISITES------------------------------------------------------------------
VIDEO_ALLOWED_EXTENSIONS = {'mp4'}
def video_allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in VIDEO_ALLOWED_EXTENSIONS
# AUDIO VALIDATION PREREQUISITES------------------------------------------------------------------
AUDIO_ALLOWED_EXTENSIONS = {'mp3'}
def audio_allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in AUDIO_ALLOWED_EXTENSIONS

import html
## MEDIA OUTPUT 
def filext(input):

    if image_allowed_file(input):
        return html.unescape('<img class="rounded mx-auto d-block" style="max-width: 200px;" src="/static/uploads/images/'+input+'">')
    elif video_allowed_file(input):
        return html.unescape('<video class="rounded mx-auto d-block" width="720" height="480" controls><source src="/static/uploads/video/'+input+'"></source></video>')
    elif audio_allowed_file(input):
        return html.unescape('<audio class="rounded mx-auto d-block" controls><source src="/static/uploads/audio/'+input+'"></source></audio>')

app.jinja_env.globals.update(filext = filext)
