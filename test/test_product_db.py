import pytest
from app import app
from your_module import Product  # Import the Product class
from bson.objectid import ObjectId

# Define test data and fixtures
@pytest.fixture
def product_instance():
    return Product()

@pytest.fixture
def sample_product_data():
    return {
        "name": "Sample Product",
        "description": "A sample product",
        "votes": 0,
        "views": 0,
        "features": []
    }

# Test cases for the Product class
def test_add_product(product_instance, sample_product_data):
    response = product_instance.add_product(sample_product_data)
    assert "ProductID" in response
    assert "message" in response

def test_get_product(product_instance, sample_product_data):
    product_id = product_instance.add_product(sample_product_data)["ProductID"]
    product = product_instance.get_product(product_id)
    assert product is not None

def test_delete_product(product_instance, sample_product_data):
    product_name = sample_product_data["name"]
    product_instance.add_product(sample_product_data)
    response, status_code = product_instance.delete_product(product_name)
    assert status_code == 200
    assert "ok" in response
    assert "message" in response

def test_add_view(product_instance, sample_product_data):
    product_id = product_instance.add_product(sample_product_data)["ProductID"]
    response, status_code = product_instance.add_view(product_id)
    assert status_code == 200
    assert "ok" in response
    assert "message" in response

def test_add_vote(product_instance, sample_product_data):
    product_id = product_instance.add_product(sample_product_data)["ProductID"]
    response, status_code = product_instance.add_vote(product_id)
    assert status_code == 200
    assert "ok" in response
    assert "message" in response

def test_remove_vote(product_instance, sample_product_data):
    product_id = product_instance.add_product(sample_product_data)["ProductID"]
    response, status_code = product_instance.remove_vote(product_id)
    assert status_code == 200
    assert "ok" in response
    assert "message" in response

def test_add_feature(product_instance, sample_product_data):
    product_id = product_instance.add_product(sample_product_data)["ProductID"]
    feature = "New Feature"
    response, status_code = product_instance.add_feature(product_id, feature)
    assert status_code == 200
    assert "ok" in response
    assert "message" in response

# Add more test cases for other methods
