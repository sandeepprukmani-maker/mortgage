import api from './api';

export const customerService = {
  async listCustomers() {
    try {
      const response = await api.get('/api/customers');
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'Failed to fetch customers';
    }
  },

  async getCustomer(id) {
    try {
      const response = await api.get(`/api/customers/${id}`);
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'Failed to fetch customer';
    }
  },

  async createCustomer(data) {
    try {
      const response = await api.post('/api/customers', data);
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'Failed to create customer';
    }
  },

  async updateCustomer(id, data) {
    try {
      const response = await api.patch(`/api/customers/${id}`, data);
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'Failed to update customer';
    }
  },
};

export default customerService;
