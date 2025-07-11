const API_BASE_URL = 'http://localhost:8000';

export interface ApiResponse<T = any> {
  data?: T;
  error?: string;
  status: number;
}

export const api = {
  // Get auth token from localStorage
  getToken: (): string | null => {
    return localStorage.getItem('token');
  },

  // Set auth token in localStorage
  setToken: (token: string): void => {
    localStorage.setItem('token', token);
  },

  // Remove auth token from localStorage
  removeToken: (): void => {
    localStorage.removeItem('token');
  },

  // Make authenticated API request
  authenticatedRequest: async <T>(
    endpoint: string, 
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> => {
    const token = api.getToken();
    
    if (!token) {
      return {
        error: 'No authentication token found',
        status: 401
      };
    }

    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
          ...options.headers,
        },
      });

      if (response.ok) {
        const data = await response.json();
        return { data, status: response.status };
      } else {
        const errorData = await response.json();
        return { 
          error: errorData.detail || 'Request failed', 
          status: response.status 
        };
      }
    } catch (error) {
      return {
        error: 'Network error',
        status: 0
      };
    }
  },

  // Make public API request (no auth required)
  publicRequest: async <T>(
    endpoint: string, 
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> => {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
      });

      if (response.ok) {
        const data = await response.json();
        return { data, status: response.status };
      } else {
        const errorData = await response.json();
        return { 
          error: errorData.detail || 'Request failed', 
          status: response.status 
        };
      }
    } catch (error) {
      return {
        error: 'Network error',
        status: 0
      };
    }
  }
}; 