def test_user_signup(client):
    """Test that a new user can successfully sign up."""
    response = client.post(
        "/auth/signup",
        json={"email": "test@google.com", "password": "securepassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@google.com"
    assert "id" in data
    assert "password" not in data # Ensure password is never returned!

def test_user_signup_duplicate_email(client):
    """Test that signing up with an existing email fails."""
    # First signup
    client.post("/auth/signup", json={"email": "test@google.com", "password": "securepassword"})
    
    # Second signup with same email
    response = client.post("/auth/signup", json={"email": "test@google.com", "password": "securepassword"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_user_login(client):
    """Test that a user can login and get a JWT token."""
    client.post("/auth/signup", json={"email": "test@google.com", "password": "securepassword"})
    
    response = client.post(
        "/auth/login",
        data={"username": "test@google.com", "password": "securepassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_user_login_incorrect_password(client):
    """Test that login fails with wrong password."""
    client.post("/auth/signup", json={"email": "test@google.com", "password": "securepassword"})
    
    response = client.post(
        "/auth/login",
        data={"username": "test@google.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
