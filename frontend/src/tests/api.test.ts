import { authAPI } from '../services/api';

// Generate unique test user data
const timestamp = Date.now();
const testUser = {
  email: `test${timestamp}@example.com`,
  password: 'Test@123456',
  username: `testuser${timestamp}`,
  first_name: 'Test',
  last_name: 'User'
};

const testCredentials = {
  email: testUser.email,
  password: testUser.password
};

// Helper function to delay execution
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

// Test registration
const testRegistration = async (): Promise<boolean> => {
  try {
    console.log('🧪 Testing user registration...');
    const response = await authAPI.register(testUser);
    console.log('✅ Registration successful:', response);
    return true;
  } catch (error) {
    console.error('❌ Registration failed:', error);
    return false;
  }
};

// Test login
const testLogin = async (): Promise<boolean> => {
  try {
    console.log('🧪 Testing user login...');
    const response = await authAPI.login(testCredentials);
    console.log('✅ Login successful:', response);
    return true;
  } catch (error) {
    console.error('❌ Login failed:', error);
    return false;
  }
};

// Test token verification
const testTokenVerification = async (): Promise<boolean> => {
  try {
    console.log('🧪 Testing token verification...');
    const response = await authAPI.verifyToken();
    console.log('✅ Token verification successful:', response);
    return true;
  } catch (error) {
    console.error('❌ Token verification failed:', error);
    return false;
  }
};

// Test logout
const testLogout = async (): Promise<boolean> => {
  try {
    console.log('🧪 Testing user logout...');
    const response = await authAPI.logout();
    console.log('✅ Logout successful:', response);
    return true;
  } catch (error) {
    console.error('❌ Logout failed:', error);
    return false;
  }
};

// Test invalid login
const testInvalidLogin = async (): Promise<boolean> => {
  try {
    console.log('🧪 Testing invalid login...');
    await authAPI.login({
      email: 'invalid@example.com',
      password: 'wrongpassword'
    });
    console.error('❌ Invalid login test failed: Should have rejected invalid credentials');
    return false;
  } catch (error) {
    console.log('✅ Invalid login test passed: Correctly rejected invalid credentials');
    return true;
  }
};

// Test API connection
const testAPIConnection = async () => {
  try {
    console.log('🧪 Testing API connection...');
    const testUser = {
      email: `test${Date.now()}@example.com`,
      password: 'Test@123456',
      username: `testuser${Date.now()}`,
      first_name: 'Test',
      last_name: 'User'
    };

    // Test registration
    console.log('Attempting registration...');
    const registerResponse = await authAPI.register(testUser);
    console.log('✅ Registration successful:', registerResponse);

    // Test login
    console.log('Attempting login...');
    const loginResponse = await authAPI.login({
      email: testUser.email,
      password: testUser.password
    });
    console.log('✅ Login successful:', loginResponse);

    // Test token verification
    console.log('Verifying token...');
    const verifyResponse = await authAPI.verifyToken();
    console.log('✅ Token verification successful:', verifyResponse);

    // Test logout
    console.log('Testing logout...');
    const logoutResponse = await authAPI.logout();
    console.log('✅ Logout successful:', logoutResponse);

    return true;
  } catch (error) {
    console.error('❌ API Test failed:', error);
    return false;
  }
};

// Run all tests
export const runTests = async (): Promise<void> => {
  console.log('🚀 Starting API test suite...');
  console.log('📝 Test user:', testUser);

  // Add a small delay between tests to avoid rate limiting
  const delayBetweenTests = 1000;

  try {
    // Test registration
    if (!await testRegistration()) {
      throw new Error('Registration test failed');
    }
    await delay(delayBetweenTests);

    // Test login
    if (!await testLogin()) {
      throw new Error('Login test failed');
    }
    await delay(delayBetweenTests);

    // Test token verification
    if (!await testTokenVerification()) {
      throw new Error('Token verification test failed');
    }
    await delay(delayBetweenTests);

    // Test invalid login
    if (!await testInvalidLogin()) {
      throw new Error('Invalid login test failed');
    }
    await delay(delayBetweenTests);

    // Test logout
    if (!await testLogout()) {
      throw new Error('Logout test failed');
    }

    console.log('🎉 All tests completed successfully!');
  } catch (error) {
    console.error('❌ Test suite failed:', error);
    throw error;
  }
};

// Run the test
export const runAPITest = async () => {
  console.log('🚀 Starting API test...');
  const result = await testAPIConnection();
  if (result) {
    console.log('🎉 All API tests passed successfully!');
  } else {
    console.error('❌ API tests failed');
  }
  return result;
};

export default runAPITest;

// Export individual test functions for use in other components
export {
  testRegistration,
  testLogin,
  testTokenVerification,
  testLogout,
  testInvalidLogin
}; 