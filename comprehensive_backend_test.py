#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for Threat Modeling Platform
Testing the specific endpoints mentioned by main agent as fixed
"""
import requests
import sys
import json
from datetime import datetime
from typing import Optional, Dict, Any

class ThreatModelingAPITester:
    def __init__(self, base_url="http://localhost:8001"):
        self.base_url = base_url
        self.token = None
        self.user_id = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []
        
        # Demo credentials provided by main agent
        self.demo_student_email = "student@example.com"
        self.demo_student_password = "student123"
        self.demo_admin_email = "admin@threatmodeling.com"
        self.demo_admin_password = "admin123"

    def log_test(self, name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name}")
        else:
            print(f"❌ {name} - {details}")
        
        self.test_results.append({
            "name": name,
            "success": success,
            "details": details,
            "response_data": response_data
        })

    def make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                    expected_status: int = 200, use_auth: bool = True) -> tuple[bool, Dict]:
        """Make HTTP request with error handling"""
        url = f"{self.base_url}/api/{endpoint}" if endpoint else f"{self.base_url}/"
        headers = {'Content-Type': 'application/json'}
        
        if use_auth and self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=10)
            else:
                return False, {"error": f"Unsupported method: {method}"}

            success = response.status_code == expected_status
            try:
                response_data = response.json()
            except:
                response_data = {"status_code": response.status_code, "text": response.text}

            return success, response_data

        except requests.exceptions.RequestException as e:
            return False, {"error": str(e)}

    def test_health_check(self):
        """Test basic health endpoints"""
        print("\n🔍 Testing Health Endpoints...")
        
        # Root endpoint
        success, response = self.make_request('GET', '', expected_status=200, use_auth=False)
        self.log_test("Root endpoint", success, 
                     "" if success else f"Failed: {response}")
        
        # Health check
        success, response = self.make_request('GET', 'health', expected_status=200, use_auth=False)
        self.log_test("Health check endpoint", success,
                     "" if success else f"Failed: {response}")

    def test_demo_authentication(self):
        """Test authentication with demo credentials"""
        print("\n🔍 Testing Demo Authentication...")
        
        # Test student login
        login_data = {
            "email": self.demo_student_email,
            "password": self.demo_student_password
        }
        
        success, response = self.make_request('POST', 'auth/login', login_data,
                                            expected_status=200, use_auth=False)
        if success and 'access_token' in response:
            self.token = response['access_token']
            if 'user' in response and 'id' in response['user']:
                self.user_id = response['user']['id']
        
        self.log_test("Demo student login", success,
                     "" if success else f"Failed: {response}", response)

        if success:
            # Test profile access
            success, response = self.make_request('GET', 'auth/profile', expected_status=200)
            self.log_test("Get student profile", success,
                         "" if success else f"Failed: {response}")

        # Test admin login
        admin_login_data = {
            "email": self.demo_admin_email,
            "password": self.demo_admin_password
        }
        
        success, response = self.make_request('POST', 'auth/login', admin_login_data,
                                            expected_status=200, use_auth=False)
        admin_token = None
        if success and 'access_token' in response:
            admin_token = response['access_token']
        
        self.log_test("Demo admin login", success,
                     "" if success else f"Failed: {response}")

    def test_specific_fixed_endpoints(self):
        """Test the specific endpoints mentioned as fixed by main agent"""
        print("\n🔍 Testing Previously Fixed Endpoints...")
        
        if not self.token:
            print("❌ No authentication token - skipping endpoint tests")
            return
        
        # Test GET /api/learning/paths (mentioned as now working)
        success, response = self.make_request('GET', 'learning/paths', expected_status=200)
        self.log_test("GET /api/learning/paths", success,
                     "" if success else f"Failed: {response}")

        # Test GET /api/scoring/stats (mentioned as now working)
        success, response = self.make_request('GET', 'scoring/stats', expected_status=200)
        self.log_test("GET /api/scoring/stats", success,
                     "" if success else f"Failed: {response}")

        # Test GET /api/scoring/leaderboard (mentioned as now working)
        success, response = self.make_request('GET', 'scoring/leaderboard', expected_status=200)
        self.log_test("GET /api/scoring/leaderboard", success,
                     "" if success else f"Failed: {response}")

        # Test POST /api/diagrams/ (mentioned as now working)
        # First get scenarios to create a valid diagram
        success, scenarios_response = self.make_request('GET', 'scenarios', expected_status=200)
        if success and scenarios_response and len(scenarios_response) > 0:
            scenario_id = scenarios_response[0].get('_id') or scenarios_response[0].get('id')
            
            diagram_data = {
                "title": "Test Diagram for API Testing",
                "description": "Testing POST /api/diagrams/ endpoint",
                "scenario_id": scenario_id,
                "diagram_data": {
                    "nodes": [
                        {"id": "node1", "type": "frontend", "position": {"x": 100, "y": 100}},
                        {"id": "node2", "type": "api", "position": {"x": 300, "y": 100}}
                    ],
                    "edges": [
                        {"id": "edge1", "source": "node1", "target": "node2"}
                    ]
                }
            }
            
            success, response = self.make_request('POST', 'diagrams/', diagram_data, expected_status=200)
            self.log_test("POST /api/diagrams/", success,
                         "" if success else f"Failed: {response}")
        else:
            self.log_test("POST /api/diagrams/", False, "No scenarios available to create diagram")

    def test_dashboard_data_endpoints(self):
        """Test endpoints that provide dashboard data"""
        print("\n🔍 Testing Dashboard Data Endpoints...")
        
        if not self.token:
            print("❌ No authentication token - skipping dashboard tests")
            return

        # Test scenarios endpoint for dashboard
        success, response = self.make_request('GET', 'scenarios', expected_status=200)
        self.log_test("Get scenarios for dashboard", success,
                     "" if success else f"Failed: {response}")

        # Test user diagrams
        success, response = self.make_request('GET', 'diagrams', expected_status=200)
        self.log_test("Get user diagrams", success,
                     "" if success else f"Failed: {response}")

        # Test learning progress
        success, response = self.make_request('GET', 'learning/progress', expected_status=200)
        self.log_test("Get learning progress", success,
                     "" if success else f"Failed: {response}")

        # Test achievements
        success, response = self.make_request('GET', 'learning/achievements', expected_status=200)
        self.log_test("Get achievements", success,
                     "" if success else f"Failed: {response}")

        # Test score history
        success, response = self.make_request('GET', 'scoring/history', expected_status=200)
        self.log_test("Get score history", success,
                     "" if success else f"Failed: {response}")

    def run_all_tests(self):
        """Run all test suites"""
        print("🚀 Starting Comprehensive Threat Modeling Platform API Tests")
        print(f"Testing against: {self.base_url}")
        
        try:
            self.test_health_check()
            self.test_demo_authentication()
            
            if not self.token:
                print("❌ Demo authentication failed - stopping tests")
                return False
                
            self.test_specific_fixed_endpoints()
            self.test_dashboard_data_endpoints()
            
        except Exception as e:
            print(f"❌ Test execution failed: {str(e)}")
            return False

        return True

    def print_summary(self):
        """Print test summary"""
        print(f"\n📊 Test Summary")
        print(f"Tests run: {self.tests_run}")
        print(f"Tests passed: {self.tests_passed}")
        print(f"Tests failed: {self.tests_run - self.tests_passed}")
        print(f"Success rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        # Print failed tests
        failed_tests = [test for test in self.test_results if not test['success']]
        if failed_tests:
            print(f"\n❌ Failed Tests ({len(failed_tests)}):")
            for test in failed_tests:
                print(f"  - {test['name']}: {test['details']}")
        
        # Print successful tests
        successful_tests = [test for test in self.test_results if test['success']]
        if successful_tests:
            print(f"\n✅ Successful Tests ({len(successful_tests)}):")
            for test in successful_tests:
                print(f"  - {test['name']}")

def main():
    """Main test execution"""
    tester = ThreatModelingAPITester()
    
    success = tester.run_all_tests()
    tester.print_summary()
    
    return 0 if success and tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())