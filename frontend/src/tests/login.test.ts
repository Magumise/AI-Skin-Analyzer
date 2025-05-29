import { authAPI } from '../services/api';

const testLogin = async () => {
  try {
    // Clear any existing tokens
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');

    console.log('Testing login with credentials...');
    const response = await authAPI.login({
      email: 'admin1@gmail.com',
      password: '12345678'
    });
    console.log('Login successful:', response);
    
    // Verify tokens were stored
    const accessToken = localStorage.getItem('access_token');
    const refreshToken = localStorage.getItem('refresh_token');
    console.log('Access token stored:', !!accessToken);
    console.log('Refresh token stored:', !!refreshToken);
    
    // Test token verification
    console.log('Testing token verification...');
    const verifyResponse = await authAPI.verifyToken();
    console.log('Token verification successful:', verifyResponse);
    
    // Test token refresh
    console.log('Testing token refresh...');
    const refreshResponse = await authAPI.refreshToken();
    console.log('Token refresh successful:', refreshResponse);
    
    return true;
  } catch (error) {
    console.error('Test failed:', error);
    // Clear tokens on failure
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    return false;
  }
};

// Run the test
testLogin().then(success => {
  console.log('Test completed:', success ? 'SUCCESS' : 'FAILED');
}); 