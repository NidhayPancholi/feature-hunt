import pytest
from app.users import Users  

# Define test data and fixtures
@pytest.fixture
def users_instance():
    return Users()

@pytest.fixture
def sample_user_data():
    return {
        "name": "John Doe",
        "email": "johndoe@example.com",
        # Add other user fields here
    }

# Test cases for the Users class
def test_add_user(users_instance, sample_user_data):
    response, status_code = users_instance.add_user(sample_user_data)
    assert status_code == 200
    assert "UserID" in response
    assert "message" in response

def test_get_user(users_instance):
    users = users_instance.get_users()
    assert isinstance(users, list)

def test_get_user_by_email(users_instance, sample_user_data):
    email = sample_user_data["email"]
    user = users_instance.get_user_by_email(email)
    assert user is not None
    assert user["email"] == email

def test_delete_user(users_instance, sample_user_data):
    user_name = sample_user_data["name"]
    response, status_code = users_instance.delete_user(user_name)
    assert status_code == 200
    assert "ok" in response
    assert "message" in response

# Add more test cases for other methods as needed
