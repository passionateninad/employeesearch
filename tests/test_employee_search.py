import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_basic_search():
    response = client.get("/api/v1/employees/search", params={ "company_id": 1, "page": 1, "page_size": 10 })
    assert response.status_code == 200
    assert 'results' in response.json()
    assert 'total' in response.json()

def test_search_status_filter():
    response = client.get("/api/v1/employees/search", params={ "company_id": 1, "page": 1, "page_size": 10, "status": 'active' })
    assert response.status_code == 200
    assert 'results' in response.json()
    assert 'total' in response.json()

def test_search_multiple_status():
    response = client.get("/api/v1/employees/search", params={ "company_id": 1, "page": 1, "page_size": 10, "status": ['active', 'terminated'] })
    assert response.status_code == 200
    assert 'results' in response.json()
    assert 'total' in response.json()

def test_search_location_department():
    response = client.get("/api/v1/employees/search", params={ "company_id": 1, "page": 1, "page_size": 10, "location": 'London', "department": 'Engineering' })
    assert response.status_code == 200
    assert 'results' in response.json()
    assert 'total' in response.json()

def test_search_all_filters():
    response = client.get("/api/v1/employees/search", params={ "company_id": 1, "page": 2, "page_size": 10, "status": 'active', "location": 'Bangalore', "department": 'HR', "position": 'Manager' })
    assert response.status_code == 200
    assert 'results' in response.json()
    assert 'total' in response.json()
