import api from './api';
import { useToastStore } from '../stores/toast';

export const pricingService = {
  async getConfig() {
    try {
      const response = await api.get('/api/pricing/config');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch UWM config:', error);
      return null;
    }
  },

  async getQuote(customerId, quoteData) {
    try {
      const response = await api.post('/api/pricing/quote', {
        customer_id: customerId,
        ...quoteData
      });

      // Show success toast
      const toastStore = useToastStore();
      toastStore.success(`Price quote received: ${response.data.best_price}`);

      return response.data;
    } catch (error) {
      // Error toast is already shown by API interceptor
      throw error.response?.data?.detail || 'Failed to request pricing quote';
    }
  },
};

export default pricingService;
