import { authAPI } from '../services/api';

export async function testLogin() {
  try {
    // Clear any existing tokens
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');

    // Test login with known credentials
    const credentials = {
      username: 'admin1@gmail.com',
      password: '12345678'
    };

    console.log('Attempting login...');
    const response = await authAPI.login(credentials);
    console.log('Login successful:', response);

    // Verify tokens are stored
    const accessToken = localStorage.getItem('access_token');
    const refreshToken = localStorage.getItem('refresh_token');
    console.log('Access token stored:', !!accessToken);
    console.log('Refresh token stored:', !!refreshToken);

    // Test token verification
    console.log('Verifying token...');
    await authAPI.verifyToken();
    console.log('Token verification successful');

    // Test token refresh
    console.log('Testing token refresh...');
    await authAPI.refreshToken();
    console.log('Token refresh successful');

    return true;
  } catch (error) {
    console.error('Test failed:', error);
    // Clear tokens on failure
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    return false;
  }
}

// Run the test
testLogin().then(success => {
  console.log('Test completed:', success ? 'PASSED' : 'FAILED');
}); 