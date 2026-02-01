import api from './api';

export const uwmService = {
  async testConnection() {
    try {
      const response = await api.post('/api/uwm/test-connection');
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'Failed to test UWM connection';
    }
  },
};

export default uwmService;
