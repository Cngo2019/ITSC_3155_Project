from flask import Flask, render_template

#hello
app = Flask(__name__)

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

    