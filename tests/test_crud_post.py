# THIS TESTING MODULE
def test_account_create_and_login(client):
    # LETS HAVE THE USER CREATE AN ACCOUNT AND THEN CHECK IF THEY CAN LOG IN
    with client:
        # Create an account called Jsmith33 with password 123 by sending a post request to /account_createion route.
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
        # login as Jsmith33
        client.post("/login", data={"username": "Jsmith33", "password": "123"})
        # Send a post request to the obtain_post_info. This will add this dummy post to our database
        client.post('/obtain_post_info', data={"post_title": "This is a testing post", "post_body":"This is the body of the post", "post_subject":"MATH"})
        # Get the HTML from the /view_all route
        response = client.get("/view_all")
        # make sure the post information is there
        assert b'This is a testing post' in response.data
        response = client.get('/post/1')
        assert b'This is the body of the post' in response.data
def test_post_update(client):
    #post_title = request.form.get('post_title')
    #post_body = request.form.get('post_body')
    #post_subject = request.form.get('post_subject', post_to_update.subject_tag)
    # Updating a post:
    with client:
        # Login as Jsmith33
        client.post("/login", data={"username": "Jsmith33", "password": "123"})
        # Send a post request to the post with ID 1 (the post we made in the previous test) to update the post
        client.post('/post/1',data={"post_title":"This is an updated post", "post_body": "1x2czy89gmichaeljolin22222111", "post_subject":"MATH"})
        # Go to view_all route
        response = client.get("/view_all")
        # Make sure contents are there
        assert b'1x2czy89gmichaeljolin22222111' in response.data
        assert b'This is an updated post' in response.data

def test_post_deletion(client):
    with client:
        client.post("/login", data={"username": "Jsmith33", "password": "123"})
        # Delete this post we just created and go to /view_all.
        client.post('post/1/delete')
        response = client.get('/view_all')
        # Make sure the info is NOT there
        assert b'This is a testing post' not in response.data

        