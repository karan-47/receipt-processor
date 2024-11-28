from fastapi.testclient import TestClient
import pytest


import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from db.db import receipts_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_receipts_db():
    # Clear the in-memory database before each test
    receipts_db.clear()
    yield
    # Clear the in-memory database after each test
    receipts_db.clear()


def test_create_receipt():
    response = client.post("/receipts/process", json={
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "total": 35.35,
        "items": [
            {"shortDescription": "Mountain Dew 12PK", "price": 6.49},
            {"shortDescription": "Emils Cheese Pizza", "price": 12.25},
            {"shortDescription": "Knorr Creamy Chicken", "price": 1.26},
            {"shortDescription": "Doritos Nacho Cheese", "price": 3.35},
            {"shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ", "price": 12.00}
        ]
    })
    assert response.status_code == 200
    assert "id" in response.json()



# Test for invalid arguments (no purchaseDate)
def test_create_receipt_invalid_args():
    response = client.post("/receipts/process", json={
        "retailer": "Target",
        "purchaseTime": "13:01",
        "total": 35.35,
        "items": [
            {"shortDescription": "Mountain Dew 12PK", "price": 6.49},
            {"shortDescription": "Emils Cheese Pizza", "price": 12.25},
            {"shortDescription": "Knorr Creamy Chicken", "price": 1.26},
            {"shortDescription": "Doritos Nacho Cheese", "price": 3.35},
            {"shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ", "price": 12.00}
        ]
    })
    assert response.status_code == 422

def test_create_receipt_invalid_item_price():
    response = client.post("/receipts/process", json={
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "total": 35.35,
        "items": [
            {"shortDescription": "Mountain Dew 12PK", "price": -6.49},
            {"shortDescription": "Emils Cheese Pizza", "price": 12.25},
            {"shortDescription": "Knorr Creamy Chicken", "price": 1.26},
            {"shortDescription": "Doritos Nacho Cheese", "price": 3.35},
            {"shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ", "price": 12.00}
        ]
    })
    assert response.status_code == 422

def test_create_receipt_invalid_item_price_type():
    response = client.post("/receipts/process", json={
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "total": 35.35,
        "items": [
            {"shortDescription": "Mountain Dew 12PK", "price": 6.49},
            {"shortDescription": "Emils Cheese Pizza", "price": 12.25},
            {"shortDescription": "Knorr Creamy Chicken", "price": 1.26},
            {"shortDescription": "Doritos Nacho Cheese", "price": 3.35},
            {"shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ", "price": "12.00a"}
        ]
    })
    assert response.status_code == 422

def test_get_receipt_points():
    # Create a receipt first
    create_response = client.post("/receipts/process", json={
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "total": 35.35,
        "items": [
            {"shortDescription": "Mountain Dew 12PK", "price": 6.49},
            {"shortDescription": "Emils Cheese Pizza", "price": 12.25},
            {"shortDescription": "Knorr Creamy Chicken", "price": 1.26},
            {"shortDescription": "Doritos Nacho Cheese", "price": 3.35},
            {"shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ", "price": 12.00}
        ]
    })
    receipt_id = create_response.json()["id"]

    # Get points for the created receipt
    points_response = client.get(f"/receipts/{receipt_id}/points")
    assert points_response.status_code == 200
    assert "points" in points_response.json()

def test_get_receipt_points_not_found():
    response = client.get("/receipts/123/points")
    assert response.status_code == 404