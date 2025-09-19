#!/usr/bin/env python3
"""
Focused test for core functionality with sample data
"""
import requests
import json

BASE_URL = "http://localhost:8001"

def test_with_sample_data():
    print("🔍 Testing with sample data...")
    
    # Login first
    login_data = {
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    # Try to register the test user first
    register_data = {
        "email": "test@example.com", 
        "password": "testpass123",
        "full_name": "Test User",
        "role": "user"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
        print(f"Register response: {response.status_code}")
    except:
        pass  # User might already exist
    
    # Login
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    if response.status_code != 200:
        print(f"❌ Login failed: {response.status_code} - {response.text}")
        return
    
    token = response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    # Get scenarios
    response = requests.get(f"{BASE_URL}/api/scenarios/", headers=headers)
    print(f"Scenarios: {response.status_code}")
    if response.status_code == 200:
        scenarios = response.json()
        print(f"Found {len(scenarios)} scenarios")
        
        if scenarios:
            scenario_id = scenarios[0]['id']
            print(f"Testing with scenario: {scenario_id}")
            
            # Get scenario details
            response = requests.get(f"{BASE_URL}/api/scenarios/{scenario_id}", headers=headers)
            print(f"Scenario details: {response.status_code}")
            
            # Create a diagram
            diagram_data = {
                "title": "Test Diagram",
                "description": "Test diagram for scenario",
                "scenario_id": scenario_id,
                "diagram_data": {
                    "nodes": [
                        {"id": "frontend", "type": "frontend", "position": {"x": 100, "y": 100}},
                        {"id": "api", "type": "api", "position": {"x": 300, "y": 100}}
                    ],
                    "edges": [
                        {"id": "edge1", "source": "frontend", "target": "api"}
                    ]
                }
            }
            
            response = requests.post(f"{BASE_URL}/api/diagrams/", json=diagram_data, headers=headers)
            print(f"Create diagram: {response.status_code}")
            if response.status_code == 200:
                diagram_id = response.json()['id']
                print(f"Created diagram: {diagram_id}")
                
                # Submit for scoring
                response = requests.post(f"{BASE_URL}/api/diagrams/{diagram_id}/submit", headers=headers)
                print(f"Submit diagram: {response.status_code}")
                
                # Try to score it
                response = requests.post(f"{BASE_URL}/api/scoring/score?diagram_id={diagram_id}&time_spent=300", headers=headers)
                print(f"Score diagram: {response.status_code}")
                if response.status_code != 200:
                    print(f"Score error: {response.text}")
    
    # Test learning paths (the failing endpoint)
    response = requests.get(f"{BASE_URL}/api/learning/paths", headers=headers)
    print(f"Learning paths: {response.status_code}")
    if response.status_code != 200:
        print(f"Learning paths error: {response.text}")

if __name__ == "__main__":
    test_with_sample_data()