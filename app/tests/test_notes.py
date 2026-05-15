import pytest

@pytest.fixture
def auth_headers(client):
    """Fixture to create a user and return the authorization headers for testing notes."""
    client.post("/auth/signup", json={"email": "notes@google.com", "password": "password"})
    response = client.post("/auth/login", data={"username": "notes@google.com", "password": "password"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_note(client, auth_headers):
    """Test that an authenticated user can create a note."""
    response = client.post(
        "/notes/",
        json={"title": "Test Note", "content": "This is a test"},
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Note"
    assert "id" in data

def test_get_my_notes(client, auth_headers):
    """Test getting all notes for the authenticated user."""
    # Create two notes
    client.post("/notes/", json={"title": "Note 1", "content": "1"}, headers=auth_headers)
    client.post("/notes/", json={"title": "Note 2", "content": "2"}, headers=auth_headers)
    
    response = client.get("/notes/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Note 1"

def test_unauthorized_access(client):
    """Test that unauthenticated users cannot create notes."""
    response = client.post("/notes/", json={"title": "Fail", "content": "Fail"})
    assert response.status_code == 401

def test_note_isolation(client, auth_headers):
    """Test that user 2 cannot read user 1's note (Step 6 Verification)."""
    # Create a note as User 1
    create_response = client.post("/notes/", json={"title": "Secret", "content": "Secret"}, headers=auth_headers)
    note_id = create_response.json()["id"]
    
    # Create User 2
    client.post("/auth/signup", json={"email": "hacker@google.com", "password": "password"})
    login_response = client.post("/auth/login", data={"username": "hacker@google.com", "password": "password"})
    hacker_headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
    
    # User 2 tries to fetch User 1's note
    fetch_response = client.get(f"/notes/{note_id}", headers=hacker_headers)
    assert fetch_response.status_code == 403
    assert fetch_response.json()["detail"] == "Not authorized to access this note"
