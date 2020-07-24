from datetime import datetime
from Blog import db, login_manager
from flask_login import UserMixin

##UserMixin
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    #req
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    #times
    tl = db.Column(db.DateTime(),default=datetime.utcnow)
    last_login = db.Column(db.DateTime(),default=datetime.utcnow, onupdate=datetime.utcnow)
    #other
    visit_count = db.Column(db.Integer,default=0)
    devices_log = db.Column(db.String())
    priv_key = db.Column(db.Text())

    posted = db.relationship('Post', backref='author', lazy=True)
   
    def __repr__(self):
        return f"User('{self.user_id}','{self.username}','{self.email}','{self.last_login}','{self.created}')"
##UserMixin
##requires a method that can uniquely identify a user
    def get_id(self):
        return(self.user_id)

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    post_filename = db.Column(db.String(25), nullable=False)
    title = db.Column(db.String(15), nullable=False)
    desc_short = db.Column(db.String(75), nullable=False)
    desc_long = db.Column(db.Text, nullable=False)
    user_username = db.Column(db.String(25), db.ForeignKey('user.username'), nullable=False)
    game_name = db.Column(db.String(15), nullable=False)
    game_filetype = db.Column(db.String(15), nullable=False)
    game_map = db.Column(db.String(15), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    image_primary = db.Column(db.String(25), nullable=False)
    image_others = db.Column(db.String(25), nullable=True)
    posted_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    private = db.Column(db.Boolean, nullable=False, default=True)
    child_file = db.Column(db.Integer, nullable=True)
    download_count = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return f"Post('{self.post_id}','{self.title}','{self.posted_date}')"




