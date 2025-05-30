import requests
import json
import time
from datetime import datetime

# API endpoints
BASE_URL = "https://ai-skin-analyzer-vmlu.onrender.com/api"
REGISTER_URL = f"{BASE_URL}/users/register/"
LOGIN_URL = f"{BASE_URL}/users/token/"

def test_registration():
    # Test data
    test_user = {
        "email": f"test_{int(time.time())}@example.com",  # Unique email using timestamp
        "username": f"testuser_{int(time.time())}",  # Unique username using timestamp
        "password": "Test@123456",
        "first_name": "Test",
        "last_name": "User",
        "age": 25,
        "sex": "male",
        "country": "US",
        "skin_type": ["normal", "sensitive"],
        "skin_concerns": ["acne", "aging"]
    }

    print(f"\n=== Starting Registration Test at {datetime.now()} ===")
    print(f"Testing with user data: {json.dumps(test_user, indent=2)}")

    try:
        # Test registration
        print("\n1. Testing Registration...")
        register_response = requests.post(REGISTER_URL, json=test_user)
        print(f"Registration Status Code: {register_response.status_code}")
        print(f"Registration Response: {json.dumps(register_response.json(), indent=2)}")

        if register_response.status_code == 201:
            print("✅ Registration successful!")
            
            # Test login with registered credentials
            print("\n2. Testing Login with registered credentials...")
            login_data = {
                "email": test_user["email"],
                "password": test_user["password"]
            }
            login_response = requests.post(LOGIN_URL, json=login_data)
            print(f"Login Status Code: {login_response.status_code}")
            print(f"Login Response: {json.dumps(login_response.json(), indent=2)}")

            if login_response.status_code == 200:
                print("✅ Login successful!")
                print("\n=== Test Completed Successfully ===")
                return True
            else:
                print("❌ Login failed!")
                return False
        else:
            print("❌ Registration failed!")
            return False

    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        return False

if __name__ == "__main__":
    test_registration() 