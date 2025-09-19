#!/usr/bin/env python3
"""
Frontend Authentication Flow Test
Tests the complete authentication flow using the demo accounts
"""
import requests
import sys
import json
from datetime import datetime

class FrontendAuthTester:
    def __init__(self, backend_url="http://localhost:8001"):
        self.backend_url = backend_url
        self.tests_run = 0
        self.tests_passed = 0
        
    def log_test(self, name: str, success: bool, details: str = ""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name}")
        else:
            print(f"❌ {name} - {details}")
    
    def test_demo_accounts(self):
        """Test both demo accounts"""
        print("\n🔍 Testing Demo Account Authentication...")
        
        # Test student account
        student_data = {
            "email": "student@example.com",
            "password": "student123"
        }
        
        try:
            response = requests.post(f"{self.backend_url}/api/auth/login", 
                                   json=student_data, timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                token = data.get('access_token')
                user = data.get('user', {})
                self.log_test("Student account login", True, 
                             f"User: {user.get('email')}, Role: {user.get('role')}")
                
                # Test token verification
                headers = {'Authorization': f'Bearer {token}'}
                verify_response = requests.get(f"{self.backend_url}/api/auth/verify", 
                                             headers=headers, timeout=10)
                self.log_test("Student token verification", 
                             verify_response.status_code == 200)
            else:
                self.log_test("Student account login", False, 
                             f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_test("Student account login", False, str(e))
        
        # Test admin account
        admin_data = {
            "email": "admin@threatmodeling.com",
            "password": "admin123"
        }
        
        try:
            response = requests.post(f"{self.backend_url}/api/auth/login", 
                                   json=admin_data, timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                token = data.get('access_token')
                user = data.get('user', {})
                self.log_test("Admin account login", True, 
                             f"User: {user.get('email')}, Role: {user.get('role')}")
                
                # Test token verification
                headers = {'Authorization': f'Bearer {token}'}
                verify_response = requests.get(f"{self.backend_url}/api/auth/verify", 
                                             headers=headers, timeout=10)
                self.log_test("Admin token verification", 
                             verify_response.status_code == 200)
            else:
                self.log_test("Admin account login", False, 
                             f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_test("Admin account login", False, str(e))
    
    def test_scenarios_access(self):
        """Test scenarios access with authentication"""
        print("\n🔍 Testing Scenarios Access...")
        
        # Login first
        login_data = {"email": "student@example.com", "password": "student123"}
        try:
            login_response = requests.post(f"{self.backend_url}/api/auth/login", 
                                         json=login_data, timeout=10)
            if login_response.status_code == 200:
                token = login_response.json().get('access_token')
                headers = {'Authorization': f'Bearer {token}'}
                
                # Test scenarios access
                scenarios_response = requests.get(f"{self.backend_url}/api/scenarios/", 
                                                headers=headers, timeout=10)
                success = scenarios_response.status_code == 200
                if success:
                    scenarios = scenarios_response.json()
                    self.log_test("Scenarios access", True, 
                                 f"Found {len(scenarios)} scenarios")
                else:
                    self.log_test("Scenarios access", False, 
                                 f"Status: {scenarios_response.status_code}")
            else:
                self.log_test("Scenarios access", False, "Login failed")
        except Exception as e:
            self.log_test("Scenarios access", False, str(e))
    
    def test_frontend_connectivity(self):
        """Test frontend service connectivity"""
        print("\n🔍 Testing Frontend Service...")
        
        try:
            # Test frontend HTML
            response = requests.get("http://localhost:3000", timeout=10)
            success = response.status_code == 200 and "<!DOCTYPE html>" in response.text
            if success:
                has_root = '<div id="root"></div>' in response.text
                has_react = 'src="/src/main.jsx"' in response.text
                self.log_test("Frontend HTML serving", True, 
                             f"Root div: {has_root}, React script: {has_react}")
            else:
                self.log_test("Frontend HTML serving", False, 
                             f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Frontend HTML serving", False, str(e))
    
    def run_all_tests(self):
        """Run all test suites"""
        print("🚀 Starting Frontend Authentication Tests")
        print(f"Backend URL: {self.backend_url}")
        
        self.test_demo_accounts()
        self.test_scenarios_access()
        self.test_frontend_connectivity()
        
        return True
    
    def print_summary(self):
        """Print test summary"""
        print(f"\n📊 Test Summary")
        print(f"Tests run: {self.tests_run}")
        print(f"Tests passed: {self.tests_passed}")
        print(f"Tests failed: {self.tests_run - self.tests_passed}")
        print(f"Success rate: {(self.tests_passed/self.tests_run)*100:.1f}%")

def main():
    """Main test execution"""
    tester = FrontendAuthTester()
    
    success = tester.run_all_tests()
    tester.print_summary()
    
    return 0 if success and tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())