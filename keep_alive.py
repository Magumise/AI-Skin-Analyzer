import requests
import time
import schedule
from datetime import datetime
import sys

# API endpoints to test
ENDPOINTS = [
    '/api/ping',
    '/api/users/test/',
    '/api/analysis/analyze/'
]

BASE_URL = 'https://ai-skin-analyzer-nw9c.onrender.com'

def test_endpoint(endpoint):
    try:
        url = f"{BASE_URL}{endpoint}"
        response = requests.get(url, timeout=30)
        return response.status_code
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

def ping_backend():
    print(f"\n[{datetime.now()}] Testing backend endpoints...")
    all_successful = True
    
    for endpoint in ENDPOINTS:
        status = test_endpoint(endpoint)
        if isinstance(status, int) and status == 200:
            print(f"✅ {endpoint}: Success (Status {status})")
        else:
            print(f"❌ {endpoint}: Failed - {status}")
            all_successful = False
    
    if all_successful:
        print(f"✅ All endpoints are working!")
    else:
        print(f"⚠️ Some endpoints failed. Backend might be spinning up...")
        # Retry after 30 seconds if any endpoint failed
        time.sleep(30)
        print("Retrying failed endpoints...")
        ping_backend()

def main():
    print("🚀 Starting keep-alive service...")
    print("⏰ Pinging backend every 14 minutes to prevent spin-down")
    print("📝 Testing endpoints:", ", ".join(ENDPOINTS))
    print("Press Ctrl+C to stop the service")
    
    # Schedule the ping every 14 minutes
    schedule.every(14).minutes.do(ping_backend)
    
    # Initial ping
    ping_backend()
    
    try:
        # Keep the script running
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Stopping keep-alive service...")
        sys.exit(0)

if __name__ == "__main__":
    main() 