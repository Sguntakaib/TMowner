#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for Threat Modeling Platform
Tests all major endpoints: Auth, Scenarios, Diagrams, Scoring, Learning
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
        
        # Test data storage
        self.test_user_email = f"test_user_{datetime.now().strftime('%H%M%S')}@example.com"
        self.test_password = "TestPass123!"
        self.scenario_ids = []
        self.diagram_ids = []
        self.score_ids = []

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
        url = f"{self.base_url}/api/{endpoint}"
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

    # ============ HEALTH CHECK ============
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

    # ============ AUTHENTICATION TESTS ============
    def test_authentication(self):
        """Test authentication flow"""
        print("\n🔍 Testing Authentication...")
        
        # Test registration
        register_data = {
            "email": self.test_user_email,
            "password": self.test_password,
            "full_name": "Test User",
            "role": "user"
        }
        
        success, response = self.make_request('POST', 'auth/register', register_data, 
                                            expected_status=200, use_auth=False)
        if success and 'access_token' in response:
            self.token = response['access_token']
            if 'user' in response and 'id' in response['user']:
                self.user_id = response['user']['id']
        
        self.log_test("User registration", success,
                     "" if success else f"Failed: {response}", response)

        # Test login
        login_data = {
            "email": self.test_user_email,
            "password": self.test_password
        }
        
        success, response = self.make_request('POST', 'auth/login', login_data,
                                            expected_status=200, use_auth=False)
        if success and 'access_token' in response:
            self.token = response['access_token']
            if 'user' in response and 'id' in response['user']:
                self.user_id = response['user']['id']
        
        self.log_test("User login", success,
                     "" if success else f"Failed: {response}", response)

        # Test profile access
        success, response = self.make_request('GET', 'auth/profile', expected_status=200)
        self.log_test("Get profile", success,
                     "" if success else f"Failed: {response}")

        # Test token verification
        success, response = self.make_request('GET', 'auth/verify', expected_status=200)
        self.log_test("Token verification", success,
                     "" if success else f"Failed: {response}")

    # ============ SCENARIO TESTS ============
    def test_scenarios(self):
        """Test scenario management"""
        print("\n🔍 Testing Scenarios...")
        
        # Get all scenarios
        success, response = self.make_request('GET', 'scenarios', expected_status=200)
        if success and isinstance(response, list):
            self.scenario_ids = [scenario.get('id') for scenario in response if scenario.get('id')]
        
        self.log_test("Get scenarios list", success,
                     "" if success else f"Failed: {response}")

        # Test filtering by category
        success, response = self.make_request('GET', 'scenarios?category=web', expected_status=200)
        self.log_test("Filter scenarios by category", success,
                     "" if success else f"Failed: {response}")

        # Test filtering by difficulty
        success, response = self.make_request('GET', 'scenarios?difficulty=beginner', expected_status=200)
        self.log_test("Filter scenarios by difficulty", success,
                     "" if success else f"Failed: {response}")

        # Get scenario details (if we have scenarios)
        if self.scenario_ids:
            scenario_id = self.scenario_ids[0]
            success, response = self.make_request('GET', f'scenarios/{scenario_id}', expected_status=200)
            self.log_test("Get scenario details", success,
                         "" if success else f"Failed: {response}")

        # Get categories
        success, response = self.make_request('GET', 'scenarios/categories/list', expected_status=200)
        self.log_test("Get scenario categories", success,
                     "" if success else f"Failed: {response}")

        # Get difficulties
        success, response = self.make_request('GET', 'scenarios/difficulties/list', expected_status=200)
        self.log_test("Get difficulty levels", success,
                     "" if success else f"Failed: {response}")

    # ============ DIAGRAM TESTS ============
    def test_diagrams(self):
        """Test diagram management"""
        print("\n🔍 Testing Diagrams...")
        
        # Get user diagrams
        success, response = self.make_request('GET', 'diagrams', expected_status=200)
        self.log_test("Get user diagrams", success,
                     "" if success else f"Failed: {response}")

        # Create a test diagram (if we have scenarios)
        if self.scenario_ids:
            diagram_data = {
                "title": "Test Diagram",
                "description": "Test diagram for API testing",
                "scenario_id": self.scenario_ids[0],
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
            
            success, response = self.make_request('POST', 'diagrams', diagram_data, expected_status=200)
            if success and 'id' in response:
                self.diagram_ids.append(response['id'])
            
            self.log_test("Create diagram", success,
                         "" if success else f"Failed: {response}")

            # Get diagram details
            if self.diagram_ids:
                diagram_id = self.diagram_ids[0]
                success, response = self.make_request('GET', f'diagrams/{diagram_id}', expected_status=200)
                self.log_test("Get diagram details", success,
                             "" if success else f"Failed: {response}")

                # Update diagram
                update_data = {
                    "title": "Updated Test Diagram",
                    "description": "Updated description"
                }
                success, response = self.make_request('PUT', f'diagrams/{diagram_id}', update_data, expected_status=200)
                self.log_test("Update diagram", success,
                             "" if success else f"Failed: {response}")

                # Submit diagram for scoring
                success, response = self.make_request('POST', f'diagrams/{diagram_id}/submit', expected_status=200)
                self.log_test("Submit diagram for scoring", success,
                             "" if success else f"Failed: {response}")

    # ============ SCORING TESTS ============
    def test_scoring(self):
        """Test scoring functionality"""
        print("\n🔍 Testing Scoring...")
        
        # Test diagram validation (if we have diagrams)
        if self.diagram_ids:
            diagram_id = self.diagram_ids[0]
            
            # Validate diagram
            success, response = self.make_request('POST', f'scoring/validate?diagram_id={diagram_id}', 
                                                expected_status=200)
            self.log_test("Validate diagram", success,
                         "" if success else f"Failed: {response}")

            # Score diagram
            success, response = self.make_request('POST', f'scoring/score?diagram_id={diagram_id}&time_spent=300',
                                                expected_status=200)
            if success and 'id' in response:
                self.score_ids.append(response['id'])
            
            self.log_test("Score diagram", success,
                         "" if success else f"Failed: {response}")

        # Get score history
        success, response = self.make_request('GET', 'scoring/history', expected_status=200)
        self.log_test("Get score history", success,
                     "" if success else f"Failed: {response}")

        # Get user stats
        success, response = self.make_request('GET', 'scoring/stats', expected_status=200)
        self.log_test("Get user statistics", success,
                     "" if success else f"Failed: {response}")

        # Get leaderboard
        success, response = self.make_request('GET', 'scoring/leaderboard', expected_status=200)
        self.log_test("Get leaderboard", success,
                     "" if success else f"Failed: {response}")

        # Get analytics
        success, response = self.make_request('GET', 'scoring/analytics', expected_status=200)
        self.log_test("Get user analytics", success,
                     "" if success else f"Failed: {response}")

    # ============ LEARNING TESTS ============
    def test_learning(self):
        """Test learning functionality"""
        print("\n🔍 Testing Learning...")
        
        # Get learning paths
        success, response = self.make_request('GET', 'learning/paths', expected_status=200)
        self.log_test("Get learning paths", success,
                     "" if success else f"Failed: {response}")

        # Get learning progress
        success, response = self.make_request('GET', 'learning/progress', expected_status=200)
        self.log_test("Get learning progress", success,
                     "" if success else f"Failed: {response}")

        # Get recommendations
        success, response = self.make_request('GET', 'learning/recommendations', expected_status=200)
        self.log_test("Get learning recommendations", success,
                     "" if success else f"Failed: {response}")

        # Get achievements
        success, response = self.make_request('GET', 'learning/achievements', expected_status=200)
        self.log_test("Get user achievements", success,
                     "" if success else f"Failed: {response}")

        # Check for new achievements
        success, response = self.make_request('POST', 'learning/achievements/check', expected_status=200)
        self.log_test("Check new achievements", success,
                     "" if success else f"Failed: {response}")

    def run_all_tests(self):
        """Run all test suites"""
        print("🚀 Starting Threat Modeling Platform API Tests")
        print(f"Testing against: {self.base_url}")
        
        try:
            self.test_health_check()
            self.test_authentication()
            
            if not self.token:
                print("❌ Authentication failed - stopping tests")
                return False
                
            self.test_scenarios()
            self.test_diagrams()
            self.test_scoring()
            self.test_learning()
            
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

def main():
    """Main test execution"""
    tester = ThreatModelingAPITester()
    
    success = tester.run_all_tests()
    tester.print_summary()
    
    return 0 if success and tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())