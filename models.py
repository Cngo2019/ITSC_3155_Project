from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

#CREATE TABLE IF NOT EXISTS app_user (
 #   account_id INT AUTO_INCREMENT,
  #  username VARCHAR(255) NOT NULL,
   # email VARCHAR(255) NOT NULL,
    # user_password  VARCHAR(255) NOT NULL,
   # first_name VARCHAR(255) NOT NULL,
   # last_name VARCHAR(255) NOT NULL,
   # PRIMARY KEY (account_id)
#);
#user class
class User(db.Model):
    __tablename__ = 'app_user'
    account_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)
    user_password = db.Column(db.String, nullable = False)
    first_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String, nullable = False)

    def __repr__(self):
        return f'User({self.username}, {self.email}, {self.password}, {self.first_name}, {self.last_name})'

#CREATE TABLE IF NOT EXISTS post (
 #   post_id INT AUTO_INCREMENT,
  #  account_id INT NOT NULL,
   # date_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    # title VARCHAR(255) NOT NULL,
    # subject_tag VARCHAR(255) NOT NULL,
    # main_text VARCHAR(255) NOT NULL,
    # PRIMARY KEY (post_id),
    # FOREIGN KEY (account_id) REFERENCES app_user(account_id)
#);
#post class
class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key = True)
    date_time = db.Column(db.Datetime, nullable = False, default=datetime.utcnow)
    title = db.Column(db.String, nullable = False)
    subject = db.Column(db.String, nullable = False)
    main_text = db.Column(db.String, nullable = False)

    #foreign key
    account_id = db.Column(db.Integer, db.ForeignKey('user.account_id'), nullable = False)
    user = db.relationship('User', backref= 'all_user_posts')

    def __repr__(self):
        return f'Post({self.date_time}, {self.title}, {self.subject}, {self.main_text})'

#reply class 

#CREATE TABLE IF NOT EXISTS reply (
    #reply_id INT AUTO_INCREMENT,
    #main_text VARCHAR(255) NOT NULL,
    #post_id INT NOT NULL,
    #account_id INT NOT NULL,
    #PRIMARY KEY (reply_id),
    #FOREIGN KEY(post_id) REFERENCES post(post_id),
    #FOREIGN KEY(account_id) REFERENCES app_user(account_id)
#);
class Reply(db.Model):
    reply_id = db.Column(db.Integer, primary_key = True)
    date_time = db.Column(db.Datetime, nullable = False, default=datetime.utcnow)
    main_text = db.Column(db.String, nullable = False)

    #foreign keys
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable = False)
    post = db.relationship('Post', backref='post_replies')

    account_id = db.Column(db.Integer, db.ForeignKey('user.account_id'), nullable = False)
    user = db.relationship('User', backref='all_user_replies')

    def __repr__(self):
        return f'Reply({self.date_time},{self.text})'





    



