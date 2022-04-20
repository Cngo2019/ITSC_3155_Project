from flask import Flask, render_template, request, redirect, abort, session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from sqlalchemy import false, true
from models import User
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
    session['user'] = username

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
temporary_singleton = []
# Go to the create page and create the HTML page
@app.get('/create')
def create():
    return render_template('create.html')

# After submitting the information to the obtain_post_info route, we can obtain
# all the neccessary info
@app.post('/obtain_post_info')
def add_post():
    # Obtain the neccessary information sent from the form
    post_title = request.form.get('post_title')
    post_body = request.form.get('post_body')
    post_subject = request.form.get('post_subject')
    tuple_data = (post_title, post_body, post_subject)
    # Just add it to the temporary structure
    temporary_singleton.append(tuple_data)
    return redirect('/view_all')
# When going to the view_all page just simply render it.
@app.get('/view_all')
def all_posts():
    return render_template('view_all.html', all_posts = temporary_singleton)


@app.get('/account_creation')
def account_creation():
    if 'user' in session:
        return redirect('/success-login')
    return render_template('account_creation.html')

@app.post('/account_creation')
def regisration():
    username = request.form.get('username', "")
    password = request.form.get('password', "")
    email = request.form.get('email', "")
    first_name = request.form.get('first_name', "")
    last_name = request.form.get('last_name', "")

    #isAnyEmpty = inputEmpty([username, password, email, first_name, last_name])
    if first_name == "" or last_name == "" or password == "" or username == "":
        return redirect('/fail-account.html')

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first() or password == "":
        return redirect('/fail-account')
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