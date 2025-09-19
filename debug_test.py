#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://localhost:8001"

# Register and login
register_data = {
    "email": "debug@example.com", 
    "password": "testpass123",
    "full_name": "Debug User",
    "role": "user"
}

try:
    response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
    print(f"Register: {response.status_code}")
except:
    pass

login_data = {"email": "debug@example.com", "password": "testpass123"}
response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
token = response.json()['access_token']
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

# Check scenarios structure
response = requests.get(f"{BASE_URL}/api/scenarios/", headers=headers)
print(f"Scenarios response: {response.status_code}")
if response.status_code == 200:
    scenarios = response.json()
    print(f"Number of scenarios: {len(scenarios)}")
    if scenarios:
        print("First scenario structure:")
        print(json.dumps(scenarios[0], indent=2, default=str))