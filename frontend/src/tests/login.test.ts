import { authAPI } from '../services/api';

export const testLogin = async () => {
  try {
    console.log('Testing login...');
    
    // Clear any existing tokens
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    
    // Test login
    const response = await authAPI.login({
      username: 'admin1',
      password: '12345678'
    });
    
    console.log('Login successful:', response);
    
    // Verify tokens are stored
    const accessToken = localStorage.getItem('access_token');
    const refreshToken = localStorage.getItem('refresh_token');
    
    if (!accessToken || !refreshToken) {
      throw new Error('Tokens not stored properly');
    }
    
    // Test token verification
    console.log('Testing token verification...');
    await authAPI.verifyToken();
    console.log('Token verification successful');
    
    // Test token refresh
    console.log('Testing token refresh...');
    await authAPI.refreshToken();
    console.log('Token refresh successful');
    
    return true;
  } catch (error) {
    console.error('Test failed:', error);
    // Clean up on failure
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    return false;
  }
};

// Run the test if this file is executed directly
if (require.main === module) {
  testLogin()
    .then(success => console.log('Test completed:', success ? 'PASSED' : 'FAILED'))
    .catch(error => console.error('Test error:', error));
} 