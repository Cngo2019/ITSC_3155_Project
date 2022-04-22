from flask import Flask, render_template, request, redirect, abort, session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from sqlalchemy import false, true
from models import User, Post
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY')

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

db.init_app(app)
bcrypt.init_app(app)

#home route
@app.get('/')
def home():
    if 'user' in session:
        return redirect('/success-login')
    return render_template('home.html')
#login route
@app.get('/login')
def login():
    return render_template('login.html')

#login session
@app.post('/login')
def logging_on():
    username = request.form.get('username','')
    password = request.form.get('password','')

    if username == '' or password == '':
        abort(400)
    

    existing_user = User.query.filter_by(username=username).first()

    if not existing_user or existing_user.account_id == 0:
        return redirect('/fail-login')

    if not bcrypt.check_password_hash(existing_user.password, password):
        return redirect('/fail-login')
    session['user'] = {'username': username,
                        'account_id': existing_user.account_id
                      }

    return redirect('/success-login')
        
#login success
@app.get('/success-login')
def login_success():
    if not 'user' in session:
        abort(401)
    return render_template('success-login.html', user=session['user'])

#login fail
@app.get('/fail-login')
def login_fail():
    return render_template('fail-login.html')
#logout post route
@app.post('/logout')
def logout():
    if 'user' not in session:
        abort(401)
    del session['user']
    return redirect('/')

# A temporary array to store our form information when creating a post.
# temporary_singleton = []
# Go to the create page and create the HTML page
@app.get('/create')
def create():
    if not 'user' in session:
        return render_template('/login.html')
    return render_template('create.html')

# After submitting the information to the obtain_post_info route, we can obtain
# all the neccessary info
@app.post('/obtain_post_info')
def add_post():
    if not 'user' in session:
        abort(404)
    # Obtain the neccessary information sent from the form
    # title
    post_title = request.form.get('post_title')
    # main text
    post_body = request.form.get('post_body')
    # the post subject
    post_subject = request.form.get('post_subject')
    
    new_post = Post(
    title=post_title, 
    subject_tag=post_subject, 
    main_text=post_body,
    account_id=session['user']['account_id']
    )

    db.session.add(new_post)
    db.session.commit()
    # Just add it to the temporary structure
    # temporary_singleton.append(tuple_data)
    return redirect('/view_all')
# When going to the view_all page just simply render it.
@app.get('/view_all')
def all_posts():
    all_posts = Post.query.all()
    return render_template('view_all.html', all_posts=all_posts)


@app.get('/account_creation')
def account_creation():
    if 'user' in session:
        return redirect('/success-login')
    return render_template('account_creation.html')

@app.post('/account_creation')
def regisration():
    # getting the information. Set to empty as default value
    username = request.form.get('username', "")
    password = request.form.get('password', "")
    email = request.form.get('email', "")
    first_name = request.form.get('first_name', "")
    last_name = request.form.get('last_name', "")
    
    # If any of the fields are empty then redirect to an account fail
    #isAnyEmpty = inputEmpty([username, password, email, first_name, last_name])
    if first_name == "" or last_name == "" or password == "" or username == "" or email == "":
        return redirect('/fail-account')
    # If any of the usernames OR emails are taken then redirect to fail
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return redirect('/fail-account')
    # Otherwise continue generating the hashed password
    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(username=username, 
    password=hashed_password, email=email, first_name=first_name, last_name=last_name)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/success-account')


@app.get('/success-account')
def success():
    return render_template('/success-account.html')

@app.get('/fail-account')
def fail():
    return render_template('/fail-account.html')

@app.get('/post/<post_id>')
def view_post(post_id):
    # grab the post we are viewing
    current_post = Post.query.filter_by(post_id=post_id).first()
    print(current_post)
    # Grab the user's name
    current_post_username = User.query.filter_by(account_id=current_post.account_id).first().username
    current_post_account_id = User.query.filter_by(account_id=current_post.account_id).first().account_id

    if 'user' in session and session['user']['account_id'] == current_post_account_id and session['user']['username'] == current_post_username:
        return render_template('post_session.html', post=current_post, username=current_post_username)

    return render_template('post.html', post=current_post, username=current_post_username)