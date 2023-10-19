import pytest
from app import app
from app.company import Company  # Import the Company class
from bson.objectid import ObjectId

# Define test data and fixtures
@pytest.fixture
def company_instance():
    return Company()

@pytest.fixture
def sample_company_data():
    return {
        "name": "Example Company",
        "description": "A sample company",
        "products": []
    }

# Test cases for the Company class
def test_add_company(company_instance, sample_company_data):
    response = company_instance.add_company(sample_company_data)
    assert "CompanyID" in response
    assert "message" in response

def test_get_company(company_instance, sample_company_data):
    company_id = company_instance.add_company(sample_company_data)["CompanyID"]
    company = company_instance.get_company(company_id)
    assert company is not None

def test_delete_company(company_instance, sample_company_data):
    company_name = sample_company_data["name"]
    company_instance.add_company(sample_company_data)
    response, status_code = company_instance.delete_company(company_name)
    assert status_code == 200
    assert "ok" in response
    assert "message" in response

def test_get_total_votes_for_company(company_instance, sample_company_data):
    company_id = company_instance.add_company(sample_company_data)["CompanyID"]
    product_id = ObjectId()  # Create a sample product ObjectId
    company_instance.add_product_to_company(company_id, product_id)
    total_votes = company_instance.get_total_votes_for_company(company_id)
    assert total_votes == 0  # You should replace this with the actual expected value

def test_add_product_to_company(company_instance, sample_company_data):
    company_id = company_instance.add_company(sample_company_data)["CompanyID"]
    product_id = ObjectId()  # Create a sample product ObjectId
    success = company_instance.add_product_to_company(company_id, product_id)
    assert success is True

# Add more test cases for other methods as needed
