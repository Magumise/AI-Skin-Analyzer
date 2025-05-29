import { describe, it, expect } from 'vitest';
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

describe('API Integration Tests', () => {
  it('should register a new user', async () => {
    const response = await authAPI.register(testUser);
    expect(response).toHaveProperty('access');
    expect(response).toHaveProperty('refresh');
  });

  it('should login with valid credentials', async () => {
    const response = await authAPI.login(testCredentials);
    expect(response).toHaveProperty('access');
    expect(response).toHaveProperty('refresh');
  });

  it('should verify the token', async () => {
    const response = await authAPI.verifyToken();
    expect(response).toBeDefined();
  });

  it('should reject invalid login', async () => {
    try {
      await authAPI.login({ email: 'invalid@example.com', password: 'wrongpassword' });
      throw new Error('Should have thrown for invalid credentials');
    } catch (error) {
      expect(error).toBeDefined();
    }
  });

  it('should logout the user', async () => {
    const response = await authAPI.logout();
    expect(response).toBeDefined();
  });
}); 