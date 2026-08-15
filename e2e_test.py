import sys
import os
import time

sys.path.append(r"C:\Users\ydtva\yatradham-seo-pipeline (16)\yatradham-seo-pipeline")

try:
    from fastapi.testclient import TestClient
    from main import app
    client = TestClient(app)
    
    print("Testing GET /")
    response = client.get("/")
    assert response.status_code == 200
    print("GET / passed")
    
    # Test batch or scrape endpoint? (with mock data)
    print("Testing GET /stats")
    response = client.get("/stats")
    print(f"Stats response: {response.status_code} {response.json()}")
    assert response.status_code == 200
    
    print("All tests passed.")
except Exception as e:
    print(f"Test failed: {e}")
