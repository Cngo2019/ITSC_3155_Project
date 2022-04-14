from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from models import User
import os

load_dotenv()

app = Flask(__name__)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABSE_URI'] = os.getenv('DATABSE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.secret_key = os.getenv('SECRET_KEY')
db.init_app(app)
bcrypt.init_app(app)
@app.get('/')
def home():
    return render_template('home.html')

@app.get('/login')
def login():
    return render_template('login.html')
from flask import Flask, render_template, request, redirect

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
    return render_template('account_creation.html')

@app.post('/account_creation')
def regisration():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')

    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(username=username, 
    password=hashed_password, email=email, first_name=first_name, last_name=last_name)

    db.session.add(new_user)
    db.session.commit()
    return redirect("success.html")
