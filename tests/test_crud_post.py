# THIS TESTING MODULE is used to just test out how to create replies, posts, and accounts.
def test_account_create_and_login(client):
    # LETS HAVE THE USER CREATE AN ACCOUNT AND THEN CHECK IF THEY CAN LOG IN
    with client:
        #@app.post('/login')
        # Our user A2 is in our database already.
        # @app.post('/account_creation')

        # getting the information. Set to empty as default value
        #username = request.form.get('username', "")
        #password = request.form.get('password', "")
        #email = request.form.get('email', "")
        #first_name = request.form.get('first_name', "")
        #last_name = request.form.get('last_name', "")
        client.post("/account_creation", data={
            "username": "Jsmith33", 
            "password": "123",
            "email": "jsmith33@gmail.com",
            "first_name": "John",
            "last_name": "Smith"
            })
        # Send data
        client.post("/login", data={"username": "Jsmith33", "password": "123"})
        response = client.get("/home")
        assert b'Jsmith33' in response.data
# Test to see if user gets send to failed screen if they 
# create an acocunt with the same username or email
def test_post_creation(client):
    with client:
        client.post("/login", data={"username": "Jsmith33", "password": "123"})
        #post_title = request.form.get('post_title')
        # main text
        # post_body = request.form.get('post_body')
        # the post subject
        # post_subject = request.form.get('post_subject')
        # This testing post will have ID 1.
        client.post('/obtain_post_info', data={"post_title": "This is a testing post", "post_body":"This is the body of the post", "post_subject":"MATH"})
        response = client.get("/view_all")

        assert b'This is a testing post' in response.data
        response = client.get('/post/1')
        assert b'This is the body of the post' in response.data
def test_post_update(client):
    #post_title = request.form.get('post_title')
    #post_body = request.form.get('post_body')
    #post_subject = request.form.get('post_subject', post_to_update.subject_tag)
    with client:
        client.post("/login", data={"username": "Jsmith33", "password": "123"})
        client.post('/post/1',data={"post_title":"This is an updated post", "post_body": "1x2czy89gmichaeljolin22222111", "post_subject":"MATH"})
        response = client.get("/view_all")
        assert b'1x2czy89gmichaeljolin22222111' in response.data
        assert b'This is an updated post' in response.data

def test_post_deletion(client):
    with client:
        client.post("/login", data={"username": "Jsmith33", "password": "123"})
        client.post('post/1/delete')
        response = client.get('/view_all')
        assert b'This is a testing post' not in response.data

        