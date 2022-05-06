# THIS TESTING MODULE is used to just test out how to create replies, posts, and accounts.
def test_reply_creation(client):
    # LETS HAVE THE USER CREATE AN ACCOUNT AND THEN CHECK IF THEY CAN LOG IN
    with client:
        client.post("/account_creation", data={
            "username": "Jsmith33", 
            "password": "123",
            "email": "jsmith33@gmail.com",
            "first_name": "John",
            "last_name": "Smith"
            })
        # Send data
        client.post("/login", data={"username": "Jsmith33", "password": "123"})
        # Create another post that is the exact same
        client.post('/obtain_post_info', data={"post_title": "This is a testing post", "post_body":"This is the body of the post", "post_subject":"MATH"})
        
        # Let's log out and create a new user called Jsmith99 and login as Jsmith 99:

        # Log out
        client.post('/logout')
        # This post will have post id 2 since we deleted a post in the previous module. Attach this reply to it
        client.post("/account_creation", data={
            "username": "Jsmith99", 
            "password": "123",
            "email": "jsmith99@gmail.com",
            "first_name": "John",
            "last_name": "Smith"
            })
        # Create a reply by Jsmith99
        client.post("/login", data={"username": "Jsmith99", "password": "123"})
        client.post('/reply/2', data={'reply_body':'1x2czy89gmichaeljolin22222111'})
        # Go to the post now.
        response = client.get('/post/2')
        assert b'1x2czy89gmichaeljolin22222111' in response.data
        assert b'Jsmith99 responded with:' in response.data
        assert b'Jsmith33' in response.data
        client.post('/logout')

def test_reply_update(client):
    with client:
        client.post("/login", data={"username": "Jsmith99", "password": "123"})
        client.post("/reply/1/delete")
        response = client.get('/post/2')
        assert b'1x2czy89gmichaeljolin22222111' not in response.data
        assert b'Jsmith99 responded with:' not in response.data
        client.post('/logout')