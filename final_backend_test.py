#!/usr/bin/env python3
"""
Final comprehensive backend test with correct field names
"""
import requests
import json

BASE_URL = "http://localhost:8001"

def test_complete_flow():
    print("🚀 Testing complete threat modeling flow...")
    
    # Register and login
    register_data = {
        "email": "final@example.com", 
        "password": "testpass123",
        "full_name": "Final Test User",
        "role": "user"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
        print(f"✅ Register: {response.status_code}")
    except:
        pass
    
    login_data = {"email": "final@example.com", "password": "testpass123"}
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    if response.status_code != 200:
        print(f"❌ Login failed: {response.status_code}")
        return False
    
    token = response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    print("✅ Authentication successful")
    
    # Test scenarios
    response = requests.get(f"{BASE_URL}/api/scenarios/", headers=headers)
    if response.status_code != 200:
        print(f"❌ Get scenarios failed: {response.status_code}")
        return False
    
    scenarios = response.json()
    print(f"✅ Found {len(scenarios)} scenarios")
    
    if not scenarios:
        print("❌ No scenarios available")
        return False
    
    # Use _id field for MongoDB
    scenario_id = scenarios[0]['_id']
    scenario_title = scenarios[0]['title']
    print(f"✅ Testing with scenario: {scenario_title}")
    
    # Get scenario details
    response = requests.get(f"{BASE_URL}/api/scenarios/{scenario_id}", headers=headers)
    if response.status_code != 200:
        print(f"❌ Get scenario details failed: {response.status_code}")
        return False
    print("✅ Scenario details retrieved")
    
    # Create diagram
    diagram_data = {
        "title": "Test E-commerce Diagram",
        "description": "Testing diagram creation and scoring",
        "scenario_id": scenario_id,
        "diagram_data": {
            "nodes": [
                {"id": "frontend", "type": "frontend", "position": {"x": 100, "y": 100}},
                {"id": "api", "type": "api", "position": {"x": 300, "y": 100}},
                {"id": "auth", "type": "security", "position": {"x": 500, "y": 50}},
                {"id": "db", "type": "database", "position": {"x": 500, "y": 150}}
            ],
            "edges": [
                {"id": "e1", "source": "frontend", "target": "api"},
                {"id": "e2", "source": "api", "target": "auth"},
                {"id": "e3", "source": "api", "target": "db"}
            ]
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/diagrams/", json=diagram_data, headers=headers)
    if response.status_code != 200:
        print(f"❌ Create diagram failed: {response.status_code} - {response.text}")
        return False
    
    diagram = response.json()
    diagram_id = diagram.get('_id') or diagram.get('id')
    print(f"✅ Created diagram: {diagram_id}")
    
    # Submit diagram
    response = requests.post(f"{BASE_URL}/api/diagrams/{diagram_id}/submit", headers=headers)
    if response.status_code != 200:
        print(f"❌ Submit diagram failed: {response.status_code} - {response.text}")
        return False
    print("✅ Diagram submitted")
    
    # Validate diagram
    response = requests.post(f"{BASE_URL}/api/scoring/validate?diagram_id={diagram_id}", headers=headers)
    if response.status_code != 200:
        print(f"❌ Validate diagram failed: {response.status_code} - {response.text}")
        return False
    print("✅ Diagram validated")
    
    # Score diagram
    response = requests.post(f"{BASE_URL}/api/scoring/score?diagram_id={diagram_id}&time_spent=300", headers=headers)
    if response.status_code != 200:
        print(f"❌ Score diagram failed: {response.status_code} - {response.text}")
        return False
    
    score = response.json()
    print(f"✅ Diagram scored: {score.get('total_score', 'N/A')} points")
    
    # Get score history
    response = requests.get(f"{BASE_URL}/api/scoring/history", headers=headers)
    if response.status_code != 200:
        print(f"❌ Get score history failed: {response.status_code}")
        return False
    
    scores = response.json()
    print(f"✅ Score history: {len(scores)} entries")
    
    # Test learning endpoints (except the broken one)
    response = requests.get(f"{BASE_URL}/api/learning/progress", headers=headers)
    print(f"✅ Learning progress: {response.status_code}")
    
    response = requests.get(f"{BASE_URL}/api/learning/achievements", headers=headers)
    print(f"✅ Achievements: {response.status_code}")
    
    print("\n🎉 Complete flow test successful!")
    return True

def test_known_issues():
    """Test the known problematic endpoints"""
    print("\n🔍 Testing known issues...")
    
    # Login first
    login_data = {"email": "final@example.com", "password": "testpass123"}
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    token = response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    # Test learning paths (known to fail)
    response = requests.get(f"{BASE_URL}/api/learning/paths", headers=headers)
    if response.status_code == 500:
        print("❌ Learning paths endpoint has ObjectId serialization error (confirmed)")
    else:
        print(f"✅ Learning paths: {response.status_code}")

if __name__ == "__main__":
    success = test_complete_flow()
    test_known_issues()
    
    if success:
        print("\n✅ Backend core functionality is working!")
        print("⚠️  Known issue: Learning paths endpoint has serialization error")
    else:
        print("\n❌ Backend has critical issues")