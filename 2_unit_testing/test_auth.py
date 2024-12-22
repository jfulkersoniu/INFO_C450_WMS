import pytest
import cluster

def test_authenticate_user_success():
    # Assuming you have a test user in the database
    username = "test_user"
    password = "correct_password"
    user = cluster.authenticate_user(username, password)
    assert user is not None
    assert user['username'] == username

def test_authenticate_user_failure():
    username = "test_user"
    password = "wrong_password"
    user = cluster.authenticate_user(username, password)
    assert user is None
