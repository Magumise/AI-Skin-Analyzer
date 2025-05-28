import requests
import json

def test_registration():
    # API endpoint
    url = 'https://ai-skin-analyzer-vmlu.onrender.com/api/users/register/'
    
    # Test user data
    data = {
        "email": "test@example.com",
        "password": "Test@123",
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User"
    }
    
    # Headers
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    print("Sending registration request...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        # Send POST request
        response = requests.post(url, json=data, headers=headers)
        
        # Print response
        print(f"\nStatus Code: {response.status_code}")
        try:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"Response: {response.text}")
        
        return response.json() if response.status_code == 201 else None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    test_registration() 