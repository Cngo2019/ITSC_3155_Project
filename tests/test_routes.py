# THIS TESTING
from models import Post, Reply, User
def test_home_route(client):
    response = client.get("/")
    assert b'<h1>Be better, learn better</h1>' in response.data
    ##
    with client:
        client.post("/account_creation", data={
            "username": "A2", 
            "password": "123",
            "email": "A2@gmail.com",
            "first_name": "John",
            "last_name": "Smith"
            })
        #@app.post('/login')
        # Our user A2 is in our database already.
        client.post("/login", data={"username": "A2", "password": "123"})
        response = client.get("/success-login")
        assert b'A2' in response.data


