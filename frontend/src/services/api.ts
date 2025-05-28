import axios from 'axios';

// API configuration
const API_URL = import.meta.env.VITE_API_URL || 'https://ai-skin-analyzer-nw9c.onrender.com/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  withCredentials: true,
  timeout: 30000, // 30 seconds
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Get token from localStorage
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Handle network errors
    if (!error.response) {
      console.error('Network error:', error);
      return Promise.reject(new Error('Network error. Please check your internet connection and try again.'));
    }

    // Handle CORS errors
    if (error.message && error.message.includes('CORS')) {
      console.error('CORS Error:', error);
      return Promise.reject(new Error('Unable to connect to the server. Please try again later.'));
    }

    // Handle 401 Unauthorized errors
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) {
          throw new Error('No refresh token available');
        }

        const response = await api.post('/users/token/refresh/', {
          refresh: refreshToken
        });

        const { access } = response.data;
        localStorage.setItem('access_token', access);

        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        console.error('Token refresh failed:', refreshError);
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/auth';
        return Promise.reject(new Error('Session expired. Please login again.'));
      }
    }

    // Handle other errors
    const errorMessage = error.response.data?.detail || error.response.data?.message || 'An error occurred';
    return Promise.reject(new Error(errorMessage));
  }
);

// Authentication API methods
export const authAPI = {
  // Register new user
  register: async (userData: any) => {
    try {
      console.log('Sending registration data:', userData);
      const response = await api.post('/users/register/', userData);
      if (response.data.access) {
        localStorage.setItem('access_token', response.data.access);
      }
      if (response.data.refresh) {
        localStorage.setItem('refresh_token', response.data.refresh);
      }
      return response.data;
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  },

  // Login user
  login: async (credentials: { email: string; password: string }) => {
    try {
      const response = await api.post('/users/login/', credentials);
      if (response.data.access) {
        localStorage.setItem('access_token', response.data.access);
      }
      if (response.data.refresh) {
        localStorage.setItem('refresh_token', response.data.refresh);
      }
      return response.data;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  },

  // Logout user
  logout: async () => {
    try {
      const response = await api.post('/users/logout/');
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      return response.data;
    } catch (error) {
      console.error('Logout error:', error);
      // Still clear tokens even if the request fails
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      throw error;
    }
  },

  // Verify token
  verifyToken: async () => {
    try {
      const response = await api.post('/users/token/verify/');
      return response.data;
    } catch (error) {
      console.error('Token verification error:', error);
      throw error;
    }
  }
};

export default api;