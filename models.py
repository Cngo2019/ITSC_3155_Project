from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


#user class
class User(db.Model):
    account_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    first_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String, nullable = False)

    def __repr__(self):
        return f'User({self.username}, {self.email}, {self.password}, {self.first_name}, {self.last_name})'

#post class
class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key = True)
    date_time = db.Column(db.Datetime, nullable = False, default=datetime.utcnow)
    title = db.Column(db.String, nullable = False)
    subject = db.Column(db.String, nullable = False)
    main_text = db.Column(db.String, nullable = False)

    account_id = db.Column(db.Integer, db.ForeignKey('user.account_id'), nullable = False)
    users = db.relationship('User', backref= 'poster')

    def __repr__(self):
        return f'Post({self.date_time}, {self.title}, {self.subject}, {self.main_text})'

#reply class 
class Reply(db.Model):
    reply_id = db.Column(db.Integer, primary_key = True)
    date_time = db.Column(db.Datetime, nullable = False, default=datetime.utcnow)
    text = db.Column(db.String, nullable = False)

    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable = False)
    posts = db.relationship('Post', backref='poster')

    account_id = db.Column(db.Integer, db.ForeignKey('user.account_id'), nullable = False)
    users = db.relationship('User', backref='replier')

    def __repr__(self):
        return f'Reply({self.text})'






    



