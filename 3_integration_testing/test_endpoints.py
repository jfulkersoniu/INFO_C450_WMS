import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_login_endpoint(client):
    response = client.post('/auth/login', data=dict(username='test_user', password='correct_password'))
    assert response.status_code == 302  # Redirects after successful login

def test_login_endpoint_failure(client):
    response = client.post('/auth/login', data=dict(username='test_user', password='wrong_password'))
    assert response.status_code == 302  # Redirects after failed login
