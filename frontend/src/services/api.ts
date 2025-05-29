import axios from 'axios';
import { ProductData } from '../types/ProductData';

// API configuration
const API_URL = import.meta.env.VITE_API_URL || 'https://ai-skin-analyzer-vmlu.onrender.com/api';

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
      if (error.code === 'ECONNABORTED') {
        console.error('Request timeout:', error);
        return Promise.reject(new Error('Request timed out. The server is taking too long to respond. Please try again.'));
      }
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
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          window.location.href = '/auth';
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

// Product API methods
export const productAPI = {
  // Get all products
  getAll: async () => {
    try {
      const response = await api.get('/products/');
      return response.data;
    } catch (error) {
      console.error('Error fetching products:', error);
      throw error;
    }
  },

  // Get a single product
  getOne: async (id: number) => {
    try {
      const response = await api.get(`/products/${id}/`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching product ${id}:`, error);
      throw error;
    }
  },

  // Create a new product
  create: async (productData: ProductData) => {
    try {
      const response = await api.post('/products/', productData);
      return response.data;
    } catch (error) {
      console.error('Error creating product:', error);
      throw error;
    }
  },

  // Update a product
  update: async (id: number, productData: ProductData) => {
    try {
      const response = await api.put(`/products/${id}/`, productData);
      return response.data;
    } catch (error) {
      console.error(`Error updating product ${id}:`, error);
      throw error;
    }
  },

  // Delete a product
  delete: async (id: number) => {
    try {
      const response = await api.delete(`/products/${id}/`);
      return response.data;
    } catch (error) {
      console.error(`Error deleting product ${id}:`, error);
      throw error;
    }
  },

  // Update product image
  updateProductImage: async (id: number, imageFile: File) => {
    try {
      const formData = new FormData();
      formData.append('image', imageFile);
      
      const response = await api.patch(`/products/${id}/image/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      console.error(`Error updating product image ${id}:`, error);
      throw error;
    }
  }
};

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
      const token = localStorage.getItem('access_token');
      if (!token) {
        throw new Error('No token available');
      }
      const response = await api.post('/users/token/verify/', { token });
      return response.data;
    } catch (error) {
      console.error('Token verification error:', error);
      throw error;
    }
  }
};

// Test AI Model endpoint
export const testAIModel = async () => {
  try {
    const response = await api.get('/test-ai-model/');
    return response.data;
  } catch (error) {
    console.error('Error testing AI model endpoint:', error);
    throw error;
  }
};

export default api;