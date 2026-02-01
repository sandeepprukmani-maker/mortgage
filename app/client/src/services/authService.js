import api from './api';

export const authService = {
  async register(email, password, firstName, lastName) {
    try {
      const response = await api.post('/api/auth/register', {
        email,
        password,
        first_name: firstName,
        last_name: lastName,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'Registration failed';
    }
  },

  async login(email, password) {
    try {
      const response = await api.post('/api/auth/login', {
        email,
        password,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'Login failed';
    }
  },

  async logout() {
    try {
      await api.post('/api/auth/logout');
      localStorage.removeItem('accessToken');
    } catch (error) {
      throw error.response?.data?.detail || 'Logout failed';
    }
  },

  async refreshToken() {
    try {
      const response = await api.post('/api/auth/refresh');
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'Token refresh failed';
    }
  },

  async getGoogleAuthUrl() {
    try {
      const response = await api.get('/api/auth/google');
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'Failed to get Google auth URL';
    }
  },

  async forgotPassword(email) {
    try {
      const response = await api.post('/api/auth/forgot-password', {
        email,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'Password reset request failed';
    }
  },

  async resetPassword(token, newPassword) {
    try {
      const response = await api.post('/api/auth/reset-password', {
        token,
        new_password: newPassword,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'Password reset failed';
    }
  },
};

export default authService;
