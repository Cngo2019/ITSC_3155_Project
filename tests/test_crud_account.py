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

#Test account read
def test_account_read(client):
    with client:
        client.post("/login", data={"username": "Jsmith33", "password": "123"})
        response = client.get('/my_account')
        assert b'<h3>Username</h3>' in response.data
        assert b'<p>Jsmith33</p>' in response.data
        assert b'<p>jsmith33@gmail.com</p>' in response.data




#Test account update 
def test_account_update(client):
    with client:
        client.post("/login", data={"username": "Jsmith33", "password": "123"})
        client.post('/username_updated', data={'edit_username': 'Jsmith500'})
        client.post('/email_updated', data={'edit_email': 'jsmith500@gmail.com'})

        response = client.get('/my_account')

        assert b'<p>Jsmith500</p>' in response.data
        assert b'<p>jsmith500@gmail.com</p>' in response.data


#Test account delete 
def test_account_delete(client):
    with client:
        client.post("/login", data={"username": "Jsmith500", "password": "123"})
        client.get('/delete_account/1')

        response = client.get('/home')
        assert b'Jsmith500' not in response.data