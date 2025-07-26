from flaskblog import db,login_manager
from datetime import datetime,timezone
from flask_login import UserMixin

#The class that you use to represent users needs to implement these properties and methods:
# is_authenticated(),is_active(),is_anonymous(),get_id()
# To make implementing a user class easier, you can inherit from UserMixin

@login_manager.user_loader
def load_user(user_id):         #simply fetches user it 'user_id', (is according to the docs-> flask_login) 
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True,)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(150),unique=True,nullable=False)
    image_file=db.Column(db.String(20),nullable=False,default='default.png')
    password=db.Column(db.String(60),nullable=False)
    post=db.relationship('Post',backref='author',lazy=True)

    def __repr__(self):
        return f"User({self.username},{self.email},{self.image_file})"

class Post(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(150),nullable=False)
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow) # Not the () since we don't want the (executed) time right now
    content=db.Column(db.Text,nullable=False)
    # The 'User' model will have atomatically set the table name as 'user' same for 'Post'->'post, tb_name can be changed. 
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)  

    def __repr__(self):
        return f"Post({self.title},{self.date_posted})"
