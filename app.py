from flask import Flask, render_template, request, redirect, abort, session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from sqlalchemy import false, true
from models import User, Post, db, Reply
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY')

bcrypt = Bcrypt(app)
#db = SQLAlchemy(app)

db.init_app(app)
bcrypt.init_app(app)

#home route
@app.get('/')
def home():
    if 'user' in session:
        return redirect('/success-login')
    return render_template('home.html')

#home page once logged in
@app.get('/home')
def loggedin_home():
    return render_template('logged-in-home.html', user=session['user'])
#user profile route
@app.get('/profile')
def profile():
    return render_template('profile.html', user=session['user'])
#login route
@app.get('/login')
def login():
    return render_template('login.html')

#login session
@app.post('/login')
def logging_on():
    username = request.form.get('username','')
    password = request.form.get('password','')

    
    

    existing_user = User.query.filter_by(username=username).first()

    if not existing_user or existing_user.account_id == 0:
        return redirect('/login')

    if not bcrypt.check_password_hash(existing_user.password, password):
        return redirect('/login')
    
    session['user'] = username

    return redirect('/success-login')
        
#login success
@app.get('/success-login')
def login_success():
    if not 'user' in session:
        abort(401)
    return render_template('logged-in-home.html', user=session['user'])

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
    return render_template('create.html', user=session['user'])

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

    if post_title == "" or post_body == "" or post_subject == "":
        return redirect('/create')
    
    # Get the account id

    user_account_id = User.query.filter_by(username=session['user']).first().account_id
    new_post = Post(
    title=post_title, 
    subject_tag=post_subject, 
    main_text=post_body,
    account_id=user_account_id
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
    return render_template('view_all.html', all_posts=all_posts, user=session['user'])


@app.get('/account_creation')
def account_creation():
    if 'user' in session:
        return redirect('/success-login')
    return render_template('account_creation.html')

@app.post('/account_creation')
def registration():
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
    hashed_password = bcrypt.generate_password_hash(password) #Should .decode('utf-8') be appended? 
    new_user = User(username=username, 
    password=hashed_password, email=email, first_name=first_name, last_name=last_name)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/success-account')


@app.get('/success-account')
def success():
    return render_template('/login.html')

@app.get('/fail-account')
def fail():
    return render_template('/fail-account.html')

@app.get('/my_account')
def my_account():
    

    if 'user' in session:
        current_user = User.query.filter_by(username=session['user']).first()
        return render_template('my_account.html', current_user=current_user)
    else:
        return redirect('/account_creation')
    
@app.get('/post/<post_id>')
def view_post(post_id):
    hasReplies = 0
    # grab the post we are viewing
    current_post = Post.query.get_or_404(post_id)
    # print(current_post)
    # Grab the user's name and the ID
    current_post_username = User.query.filter_by(account_id=current_post.account_id).first().username
    current_post_account_id = User.query.filter_by(account_id=current_post.account_id).first().account_id

    # obtain all the posts that have post_id == post_id
    all_replies = Reply.query.filter_by(post_id=post_id).all()

    reply_to_be_passed_in = []
    for reply in all_replies:
        reply_data = {}
        reply_data['main_text'] = reply.main_text
        reply_data['username'] = User.query.filter_by(account_id=reply.account_id).first().username
        if reply.account_id == User.query.filter_by(username=session['user']).first().account_id:
            hasReplies = 1
        reply_to_be_passed_in.append(reply_data)
    print(hasReplies)
    if 'user' in session and session['user'] == current_post_username and current_post.account_id == current_post_account_id:
        return render_template('post_current_session.html', post=current_post, username=current_post_username, user=session['user'], replies=reply_to_be_passed_in, hasReplies=hasReplies)
    
    return render_template('post.html', post=current_post, username=current_post_username, user=session['user'], replies=reply_to_be_passed_in, hasReplies=hasReplies)

@app.get('/post/<post_id>/edit')
def get_edit_post_form(post_id):
    post_to_update = Post.query.get_or_404(post_id)
    return render_template('edit_post_form.html', post=post_to_update, user=session['user'])

@app.post('/post/<post_id>')
def update_post(post_id):
    # Get the current post
    post_to_update = Post.query.get_or_404(post_id)
    # Get the post title
    post_title = request.form.get('post_title')
    post_body = request.form.get('post_body')
    post_subject = request.form.get('post_subject', post_to_update.subject_tag)
    post_to_update.title = post_title
    post_to_update.main_text = post_body
    post_to_update.subject_tag = post_subject

    db.session.commit()
    return redirect(f'/post/{post_id}')


@app.post('/post/<post_id>/delete')
def delete_post(post_id):
    # Delete all replies associated with this post.
    child_replies = Reply.query.filter_by(post_id=post_id).all()
    for reply in child_replies:
        db.session.delete(reply)
    post_to_delete = Post.query.get_or_404(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect('/view_all')

@app.get('/user_posts/<account_id>')
def user_posts(account_id):
    ###
    all_posts = Post.query.filter_by(account_id=account_id).all()
    return render_template('view_all.html', all_posts=all_posts)

@app.get('/edit_account.html')
def edit_account():
    current_user = User.query.filter_by(username=session['user']).first()
    return render_template('edit_account.html', current_user=current_user)


@app.get('/delete_account/<account_id>')
def delete_account(account_id): #I need to pass the account id here.
    #print("Hello")

    # Get all the posts associated with the account ID
    #     delete them all
    # then proceed
    #
    all_user_replies = Reply.query.filter_by(account_id=account_id).all()
    for reply in all_user_replies:
        db.session.delete(reply)
    
    all_user_posts = Post.query.filter_by(account_id=account_id).all()
    for post in all_user_posts:
        db.session.delete(post)

    account_to_delete = User.query.get_or_404(account_id)
    
    db.session.delete(account_to_delete)
    db.session.commit()



    if 'user' not in session:
        abort(401)
    del session['user']

    return redirect("/login")

@app.get('/account_updated')
def account_edited():
    return redirect("/login") 

@app.get('/unavailable')
def unavailable():
    return render_template('unavailable.html')

@app.post('/username_updated')
def username_updated():
    if not 'user' in session:
        abort(404)
    current_user = User.query.filter_by(username=session['user']).first()
    print(current_user)
    username= request.form.get('edit_username',"")
    if User.query.filter_by(username=username).first():
        return redirect('/unavailable')
    if username == '':
        return redirect('/unavailable')
    current_user.username = username
    db.session.commit()
    session['user'] = username
    return redirect('/my_account')

@app.post('/email_updated')
def email_updated():
    if not 'user' in session:
        abort(404)
    current_user = User.query.filter_by(username=session['user']).first()
    email = request.form.get('edit_email', "")
    if User.query.filter_by(email=email).first():
        return redirect('/unavailable')
    if email == '':
        return redirect('/unavailable')
    current_user.email = email
    db.session.commit()
    return redirect('/my_account')

@app.post('/password_updated')
def password_updated():
    if not 'user' in session:
        abort(404)
    current_user = User.query.filter_by(username=session['user']).first()
    password = request.form.get('edit_password', "")
    print(password)
    if password == "":
        return redirect('/unavailable')
    hashed_password = bcrypt.generate_password_hash(password)
    current_user.password = hashed_password
    db.session.commit()
    return redirect('/my_account')

#The  session dictionary was not updated. It must be updated 
@app.get('/create-reply/<post_id>')
def create_reply(post_id):
    return render_template("create_reply.html", post_id=post_id)

@app.post('/reply/<post_id>')
def add_reply(post_id):
    reply_body = request.form.get('reply_body')
    account_id = User.query.filter_by(username=session['user']).first().account_id
    new_reply = Reply(
        main_text = reply_body,
        post_id = post_id,
        account_id = account_id
    )

    db.session.add(new_reply)
    db.session.commit()
    return redirect(f"/post/{post_id}")


@app.get('/about')
def about():
    return render_template('/about.html')

@app.get('/user_replies/<account_id>')
def load_replies(account_id):
    # get user's account ID
    account_id = User.query.filter_by(username=session['user']).first().account_id
    my_replies = []
    user_replies = Reply.query.filter_by(account_id=account_id).all()

    for reply in user_replies:
        reply_info = dict()
        post_id = reply.post_id
        post_title = Post.query.filter_by(post_id=post_id).first().title
        post_question = Post.query.filter_by(post_id=post_id).first().main_text
        reply_info['post_title'] = post_title
        reply_info['post_question'] = post_question
        reply_info['response'] = reply.main_text
        reply_info['date'] = reply.date_time
        reply_info['reply_id'] = reply.reply_id
        my_replies.append(reply_info)
    return render_template("my_replies.html", my_replies = my_replies)

@app.get('/reply/<reply_id>/edit')
def edit_reply(reply_id):
    current_reply = Reply.query.filter_by(reply_id=reply_id).first()
    return render_template('edit_reply_form.html', reply=current_reply)

@app.post('/reply/<reply_id>/edit')
def update_reply(reply_id):
    updated_text = request.form.get('reply_body')
    current_reply = Reply.query.filter_by(reply_id=reply_id).first()
    current_reply.main_text = updated_text
    db.session.commit()

    user_id = current_reply.account_id
    return redirect(f'/user_replies/{user_id}')

@app.post('/reply/<reply_id>/delete')
def delete_reply(reply_id):
    reply_to_delete = Reply.query.filter_by(reply_id=reply_id).first()
    user_id = reply_to_delete.account_id
    db.session.delete(reply_to_delete)
    db.session.commit()
    return redirect(f'/user_replies/{user_id}') 

@app.get('/my_replies/<post_id>')
def view_replies_for_specific_post(post_id):
    my_replies = []
    # Get user's acc id
    user_id = User.query.filter_by(username=session['user']).first().account_id
    user_replies = Reply.query.filter_by(post_id=post_id).filter_by(account_id=user_id).all()

    for reply in user_replies:
        reply_info = dict()
        post_title = Post.query.filter_by(post_id=post_id).first().title
        post_question = Post.query.filter_by(post_id=post_id).first().main_text
        reply_info['post_title'] = post_title
        reply_info['post_question'] = post_question
        reply_info['response'] = reply.main_text
        reply_info['date'] = reply.date_time
        reply_info['reply_id'] = reply.reply_id
        my_replies.append(reply_info)
    return render_template("my_replies.html", my_replies = my_replies)

@app.post('/post_search')
def posts_by_title():
    # This code was referenced from the SQLAlchemy flask assignment where we had to implement a function to search for movies -Can
    movie_title = request.form.get('title')
    title = f'%{movie_title}%'
    all_posts = Post.query.filter(Post.title.ilike(title)).all()
    return render_template('view_all.html', all_posts=all_posts, user=session['user'])
