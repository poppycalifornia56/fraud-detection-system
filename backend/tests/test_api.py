import requests
import json
import random

def test_create_transaction():
    """Test creating a new transaction"""
    transaction = {
        "amount": random.uniform(1000, 50000),
        "vendor_id": random.randint(1, 20),
        "department_id": random.randint(1, 8),
        "description": "Test transaction"
    }
    
    response = requests.post("http://localhost:8000/transactions/", json=transaction)
    
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["amount"] == transaction["amount"]
    
    print("✅ Create transaction test passed")
    return data["id"]

def test_get_transactions():
    """Test retrieving transactions"""
    response = requests.get("http://localhost:8000/transactions/")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    
    print("✅ Get transactions test passed")

def test_get_alerts():
    """Test retrieving alerts"""
    response = requests.get("http://localhost:8000/alerts/")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    
    print("✅ Get alerts test passed")

if __name__ == "__main__":
    try:
        transaction_id = test_create_transaction()
        test_get_transactions()
        test_get_alerts()
        print("All tests passed!")
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")