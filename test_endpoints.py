import requests
import json
from datetime import datetime

BASE_URL = 'https://ai-skin-analyzer-vmlu.onrender.com/api'

def print_response(response, title):
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")
    print(f"{'='*50}\n")

def test_endpoints():
    # Headers for JSON requests
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    # 1. Test API Documentation
    print("\nTesting API Documentation...")
    response = requests.get('https://ai-skin-analyzer-vmlu.onrender.com/')
    print_response(response, "API Documentation")

    # 2. Test Registration
    print("\nTesting User Registration...")
    registration_data = {
        "email": f"test_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com",
        "password": "Test@123",
        "username": f"testuser_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "first_name": "Test",
        "last_name": "User"
    }
    response = requests.post(f"{BASE_URL}/users/register/", json=registration_data, headers=headers)
    print_response(response, "Registration Response")
    
    if response.status_code == 201:
        tokens = response.json().get('tokens', {})
        access_token = tokens.get('access')
        refresh_token = tokens.get('refresh')
        
        # Update headers with access token
        headers['Authorization'] = f'Bearer {access_token}'
        
        # 3. Test Login
        print("\nTesting Login...")
        login_data = {
            "email": registration_data['email'],
            "password": registration_data['password']
        }
        response = requests.post(f"{BASE_URL}/token/", json=login_data, headers=headers)
        print_response(response, "Login Response")
        
        # 4. Test User Profile
        print("\nTesting User Profile...")
        response = requests.get(f"{BASE_URL}/users/", headers=headers)
        print_response(response, "User Profile Response")
        
        # 5. Test Token Refresh
        print("\nTesting Token Refresh...")
        refresh_data = {
            "refresh": refresh_token
        }
        response = requests.post(f"{BASE_URL}/token/refresh/", json=refresh_data, headers=headers)
        print_response(response, "Token Refresh Response")
        
        # 6. Test Test Endpoint
        print("\nTesting Test Endpoint...")
        response = requests.get(f"{BASE_URL}/test/", headers=headers)
        print_response(response, "Test Endpoint Response")
    else:
        print("Registration failed, skipping subsequent tests")

if __name__ == "__main__":
    test_endpoints() 