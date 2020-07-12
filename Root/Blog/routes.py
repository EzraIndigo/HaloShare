import os
from os.path import join, dirname, realpath
from datetime import datetime
from flask import Flask, render_template, flash, redirect, send_from_directory, request, url_for
from flask_login import login_user, current_user, logout_user
from Blog import app, db, bcrypt
from Blog.forms import Sign_Up_Form, Login_Form, New_Post_Form
from Blog.model import User, Post

# image
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict

# geolocate
import ipapi
import json

# ENCRYPTION libs
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

# ENCRYPTION METHODS - Fernet / small amounts of infomation
def fkey(input):  # creates keys for users
    salt = os.urandom(6)
    key = input.encode()
    kdf = PBKDF2HMAC(  # settings for key to be made with
        algorithm=hashes.SHA256(),  # hash set to use
        length=12,
        salt=salt,
        iterations=999999,  # more the merrier
        backend=default_backend()  # the backend for this all to put together with
    )

    key = base64.urlsafe_b64encode(kdf.derive(key))  # building it
    return key

# --------------------------------------------------------------- CHANGE BEFORE SUBMITTING/ TEMP BECAUSE OF REBOOTS/ SHOULD BE THE FUNCTION
storekey = b'LUBQ0ohhwDoA8U0Z'
app.jinja_env.globals['storekey'] = storekey


def fencrypt(input, client_key):

    if not isinstance(input, bytes):
        input = input.encode()

    key = b"".join([client_key, storekey])
    key = base64.urlsafe_b64encode(key)  # building it

    f = Fernet(key)

    encrypted = f.encrypt(input)
    return encrypted.decode()


def fdecrypt(input, client_key):

    if not isinstance(input, bytes):
        input = input.encode()

    key = b"".join([client_key, storekey])
    key = base64.urlsafe_b64encode(key)  # building it

    f = Fernet(key)

    decrypted = f.decrypt(input)
    return decrypted


@app.route("/")
@app.route("/home")
def home():
    post = Post.query.all()
    if not current_user.is_authenticated:
        flash(f"We see you're not signed in. You can still view publicly available posts.\n Why not make an account?", 'danger')
    return render_template('home.html', title='home', post=post)


@app.route("/profile")
def profile():
    post = Post.query.all()
    return render_template('profile.html', title='profile', post=post)


@app.route("/browse")
def groups():
    return render_template('browse.html', title='browse')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect("/home")
    form = Login_Form()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):

            ##Connected User Infomation##

            #user counter
            user.visit_count += 1

            # ENCRYPT
            db.session.add(user)
            db.session.commit()
            # login
            login_user(user)
            # flash
            flash(f'Welcome back {form.username.data.title()}.', 'success')
            return redirect('/home')
        else:
            flash(f'Wrong username or password.\n Please try again.', 'danger')

    return render_template('login.html', title='login', form=form, storekey=storekey)


@app.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect("/home")
    form = Sign_Up_Form()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        hashed_email = bcrypt.generate_password_hash(
            form.email.data).decode('utf-8')
        # --------------------------------------------------------------------------------------------ENCRYPTION--client key
        ckey = fkey(form.password.data)
        user = User(username=form.username.data, email=hashed_email,
                    password=hashed_password, priv_key=ckey)
        db.session.add(user)
        db.session.commit()
#CREATE DIRECTORY 
"""
test out making dirs in py
"""
        flash(f'Account Created. \n Thank you. \nPlease login.', 'success')
        return redirect('/home')
    return render_template('sign_up.html', title='sign up', form=form)


# -------------------------------------------------------------------------------------------------
# FILE VALIDATION PREREQUISITES------------------------------------------------------------------
IMAGE_ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
FILE_ALLOWED_EXTENSIONS = {'zip'}

def image_allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in IMAGE_ALLOWED_EXTENSIONS

def file_allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in FILE_ALLOWED_EXTENSIONS
# allowing the app to save to the correct relative path
IMAGE_UPLOAD_FOLDER = './user/uploads/images'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['IMAGE_UPLOAD_FOLDER'] = IMAGE_UPLOAD_FOLDER


# -------------------------------------------------------------------------------------------------
# POST ROUTE
@app.route("/new_post", methods=['GET', 'POST'])
def new_post():
    if not current_user.is_authenticated:
        return redirect("/home")
    else:
        form = New_Post_Form(CombinedMultiDict((request.files, request.form)))
        if form.validate_on_submit():
            # creating var if it none existent == NONE

            image = request.files['image']
            if image:
                if image_allowed_file(image.filename):
                    name = secure_filename(image.filename)
                    # creating GUID naming convention
                    timestamp = datetime.now().strftime("%m%d%Y%H%M%S")
                    filename = timestamp+name  # concatonate GUID + OG name
                if image_allowed_file(image.filename):
                    # saving to dir
                    image.save(os.path.join(
                        basedir, app.config['IMAGE_UPLOAD_FOLDER'], filename))
                else:
                    flash(f'Image upload error. Try a different image. \n', 'warning')
#unfinished start
"""
            file = request.files['file']
            if file:
                if image_allowed_file(file.filename):
                    name = secure_filename(file.filename)
                    # creating GUID naming convention
                    timestamp = datetime.now().strftime("%m%d%Y%H%M%S")
                    filename = timestamp+name  # concatonate GUID + OG name
                if image_allowed_file(file.filename):
                    # saving to dir
                    file.save(os.path.join(
                        basedir, app.config['IMAGE_UPLOAD_FOLDER'], filename))
                else:
                    flash(f'File upload error. Try a different file. \n', 'warning')
"""
#unfinished end

                # Encrypt
                if form.private.data == True:
                    form.title.data = fencrypt(
                        form.title.data, current_user.priv_key)
                    form.content.data = fencrypt(
                        form.content.data, current_user.priv_key)
                    filename = fencrypt(filename, current_user.priv_key)
                # POST
                post = Post(user_id=current_user.user_id, title=form.title.data,
                            content=form.content.data, images=filename, private=form.private.data)
                db.session.add(post)
                db.session.commit()
                flash(f'posted! \n', 'success')
            else:
                # Encrypt
                if form.private.data == True:
                    form.title.data = fencrypt(
                        form.title.data, current_user.priv_key)
                    form.content.data = fencrypt(
                        form.content.data, current_user.priv_key)
                post = Post(user_id=current_user.user_id, images='', title=form.title.data,
                            content=form.content.data, private=form.private.data)
                db.session.add(post)
                db.session.commit()
                flash(f'posted! \n', 'success')
            return redirect('/home')
    return render_template('new_post.html', title='new post', form=form)


@app.route("/post/<int:post_id>/edit", methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post:
        if current_user.user_id == post.user_id:
            form = New_Post_Form(CombinedMultiDict(
                (request.files, request.form)))
            if form.validate_on_submit():
                # FILE CHECK
                file = request.files['file']
                if file:
                    if image_allowed_file(file.filename) or video_allowed_file(file.filename) or audio_allowed_file(file.filename):
                        name = secure_filename(file.filename)
                        # creating GUID naming convention
                        timestamp = datetime.now().strftime("%m%d%Y%H%M%S")
                        filename = timestamp+name  # concatonate GUID + OG name
                        if image_allowed_file(file.filename):
                            # saving to dir
                            file.save(os.path.join(
                                basedir, app.config['IMAGE_UPLOAD_FOLDER'], filename))
                        elif video_allowed_file(file.filename):
                            # saving to dir
                            file.save(os.path.join(
                                basedir, app.config['VIDEO_UPLOAD_FOLDER'], filename))
                        elif audio_allowed_file(file.filename):
                            # saving to dir
                            file.save(os.path.join(
                                basedir, app.config['AUDIO_UPLOAD_FOLDER'], filename))
                        else:
                            flash(f'File upload error. Try a different file. \n', 'warning')
                        # Encrypt
                        if form.private.data == True:
                            form.title.data = fencrypt(form.title.data, current_user.priv_key)
                            form.content.data = fencrypt(form.content.data, current_user.priv_key)
                            filename = fencrypt(filename, current_user.priv_key)
                        # POST
                            post.title = form.title.data
                            post.content = form.content.data
                            post.image = filename
                            post.private = form.private.data
                            db.session.commit()
                            flash(f'Post edited! \n', 'success')
                            return redirect('/home')
                    else:
                        flash(
                            f'File upload error. Try a different file. \n', 'warning')
                else:
                    if form.private.data == True:
                        form.title.data = fencrypt(form.title.data, current_user.priv_key)
                        form.content.data = fencrypt(form.content.data, current_user.priv_key)
                    post.title = form.title.data
                    post.content = form.content.data
                    post.private = form.private.data
                    db.session.commit()
                    flash(f'posted! \n', 'success')
                    return redirect('/home')

            elif request.method == 'GET':
                form.title.data = post.title
                form.content.data = post.content
                form.private.data = post.private

        else:
            flash("Oops, you shouldn't be trying that.", 'warning')
    else:
        flash('Oops. Something went wrong. Please try again', 'warning')

    return render_template('new_post.html', title='edit post', form=form, post=post)

@app.route("/post/<int:post_id>/delete", methods=['POST'])
def remove_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post:
        if current_user.user_id == post.user_id:
            db.session.delete(post)
            db.session.commit()
            flash('Post deleted', 'success')
        else:
            flash('Warning. Post has not been deleted.', 'warning')
    else:
        flash('Warning. Post not found.', 'warning')

    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route('/logout')
def logout():
    logout_user()
    return redirect("/home")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Notes
#
# browser = request.user_agent.browser
# platform = request.user_agent.platform
# version = request.user_agent.version
# lang = request.user_agent.language
# if priv then encrypt
