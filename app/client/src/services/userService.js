import api from './api';

export const userService = {
  async getCurrentUser() {
    try {
      const response = await api.get('/api/users/me');
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'Failed to fetch user profile';
    }
  },

  async updateProfile(data) {
    try {
      const response = await api.patch('/api/users/me', data);
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'Failed to update profile';
    }
  },
};

export default userService;
