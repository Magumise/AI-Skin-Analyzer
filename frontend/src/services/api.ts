import axios, { InternalAxiosRequestConfig } from 'axios';
import { ProductData } from '../types/ProductData';

// Extend the AxiosRequestConfig type
interface CustomAxiosRequestConfig extends InternalAxiosRequestConfig {
  retry?: number;
  retryDelay?: number;
}

// API configuration
const API_BASE_URL = 'https://ai-skin-analyzer-vmlu.onrender.com';
const PROXY_BASE_URL = 'https://ai-skin-analyzer-proxy.onrender.com';
const API_URL = `${API_BASE_URL}/api`;

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  withCredentials: false,  // Set to false for CORS
  timeout: 60000, // Increased timeout to 60 seconds
  validateStatus: function (status) {
    return status >= 200 && status < 500; // Accept all status codes less than 500
  }
});

// Request interceptor
api.interceptors.request.use(
  (config: CustomAxiosRequestConfig) => {
    // Get token from localStorage
    const token = localStorage.getItem('access_token');
    const isAdmin = localStorage.getItem('is_admin') === 'true';
    
    // For admin, use the admin token
    if (isAdmin && token) {
      config.headers.Authorization = `Bearer ${token}`;
      // Add admin flag to headers
      config.headers['X-Admin'] = 'true';
    } else if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    // Add retry logic for failed requests
    config.retry = 3;
    config.retryDelay = 1000;
    
    // Log request details in development
    if (process.env.NODE_ENV === 'development') {
      console.log('Request:', {
        url: config.url,
        method: config.method,
        headers: config.headers,
        data: config.data
      });
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
  (response) => {
    // Log response details in development
    if (process.env.NODE_ENV === 'development') {
      console.log('Response:', {
        status: response.status,
        data: response.data,
        headers: response.headers
      });
    }
    return response;
  },
  async (error) => {
    const originalRequest = error.config;
    const isAdmin = localStorage.getItem('is_admin') === 'true';

    // For admin, skip error handling and retry with admin token
    if (isAdmin) {
      originalRequest.headers.Authorization = 'Bearer admin-token';
      originalRequest.headers['X-Admin'] = 'true';
      return api(originalRequest);
    }

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

    // Handle 502 Bad Gateway
    if (error.response.status === 502) {
      console.error('Bad Gateway Error:', error);
      return Promise.reject(new Error('Server is temporarily unavailable. Please try again in a few moments.'));
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
    const errorMessage = error.response.data?.detail || 
                        error.response.data?.message || 
                        error.response.data?.non_field_errors?.[0] ||
                        'An error occurred';
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
      console.log('Registration response:', response.data);
      
      if (response.data.tokens?.access) {
        localStorage.setItem('access_token', response.data.tokens.access);
      }
      if (response.data.tokens?.refresh) {
        localStorage.setItem('refresh_token', response.data.tokens.refresh);
      }
      return response.data;
    } catch (error: any) {
      console.error('Registration error details:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status,
        headers: error.response?.headers
      });
      
      // Handle field-specific errors
      if (error.response?.data) {
        const errorData = error.response.data;
        // If we have field-specific errors, format them
        if (typeof errorData === 'object') {
          const fieldErrors = Object.entries(errorData)
            .map(([field, messages]) => {
              const message = Array.isArray(messages) ? messages[0] : messages;
              return `${field.charAt(0).toUpperCase() + field.slice(1)}: ${message}`;
            })
            .join('\n');
          throw new Error(fieldErrors || 'Registration failed');
        }
      }
      
      // Handle network errors
      if (!error.response) {
        throw new Error('Network error. Please check your internet connection and try again.');
      }
      
      // Handle other errors
      const errorMessage = error.response?.data?.error || 
                          error.response?.data?.detail || 
                          error.response?.data?.message || 
                          error.message || 
                          'Registration failed';
      throw new Error(errorMessage);
    }
  },

  // Login user
  login: async (credentials: { email: string; password: string }) => {
    try {
      console.log('Attempting login with:', { email: credentials.email });
      
      // For all users, proceed with normal authentication
      const response = await api.post('/users/token/', {
        email: credentials.email,
        password: credentials.password
      });

      console.log('Login response:', response.data);
      
      if (!response.data.access) {
        console.error('No access token in response:', response.data);
        throw new Error('Invalid response from server');
      }

      // Store tokens
      localStorage.setItem('access_token', response.data.access);
      if (response.data.refresh) {
        localStorage.setItem('refresh_token', response.data.refresh);
      }

      // Set admin flag if user is staff or superuser
      if (response.data.user?.is_staff || response.data.user?.is_superuser) {
        localStorage.setItem('is_admin', 'true');
      }

      // Return the full response data
      return response.data;
    } catch (error: any) {
      console.error('Login error details:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status,
        headers: error.response?.headers
      });
      
      // Handle specific error cases
      if (error.response?.data?.detail) {
        throw new Error(error.response.data.detail);
      } else if (error.response?.data?.non_field_errors) {
        throw new Error(error.response.data.non_field_errors[0]);
      } else if (error.response?.data?.email) {
        throw new Error(error.response.data.email[0]);
      }
      
      throw new Error(error.message || 'Login failed');
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
      const isAdmin = localStorage.getItem('is_admin') === 'true';
      
      // For admin, skip verification
      if (isAdmin && token === 'admin-token') {
        return { valid: true };
      }

      if (!token) {
        throw new Error('No token available');
      }
      const response = await api.post('/users/token/verify/', { token });
      return response.data;
    } catch (error: any) {
      console.error('Token verification error:', error);
      if (error.response?.status === 401 || error.response?.status === 400) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('is_admin');
      }
      throw error;
    }
  },

  // Refresh token
  refreshToken: async () => {
    try {
      const refreshToken = localStorage.getItem('refresh_token');
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }
      const response = await api.post('/users/token/refresh/', {
        refresh: refreshToken
      });
      if (response.data.access) {
        localStorage.setItem('access_token', response.data.access);
      }
      return response.data;
    } catch (error) {
      console.error('Token refresh error:', error);
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
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

export const analysisAPI = {
  analyzeImage: async (imageFile: File) => {
    try {
      console.log('Sending image to proxy server...');
      const formData = new FormData();
      formData.append('file', imageFile);

      const response = await axios.post(
        `${PROXY_BASE_URL}/predict`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Accept': 'application/json'
          },
          timeout: 120000, // 120 seconds timeout
          withCredentials: false // Important for CORS
        }
      );

      console.log('Received response from proxy:', response.data);
      return response.data;
    } catch (error: any) {
      console.error('Analysis error details:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status,
        headers: error.response?.headers
      });

      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        throw new Error(error.response.data?.message || error.response.data?.error || 'Analysis failed');
      } else if (error.request) {
        // The request was made but no response was received
        throw new Error('No response received from AI model. Please check your internet connection.');
      } else {
        // Something happened in setting up the request that triggered an Error
        throw new Error(error.message || 'Analysis failed');
      }
    }
  },
};

export default api;