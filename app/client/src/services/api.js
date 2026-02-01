import axios from 'axios';
import { useLoadingStore } from '../stores/loading';
import { useToastStore } from '../stores/toast';
import { useAuthStore } from '../stores/auth';
import { useUserStore } from '../stores/user';
import router from '../router';

// Use VITE_API_URL if defined (even if empty string for relative URLs), otherwise fallback to localhost
const API_URL = import.meta.env.VITE_API_URL !== undefined ? import.meta.env.VITE_API_URL : 'http://localhost:8000';

// Extract error message from response
const getErrorMessage = (error) => {
  if (error.response?.data?.detail) {
    return error.response.data.detail;
  }
  if (error.response?.data?.message) {
    return error.response.data.message;
  }
  if (error.message) {
    return error.message;
  }
  return 'An unexpected error occurred';
};

const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
};

api.interceptors.request.use(
  (config) => {
    const loadingStore = useLoadingStore();
    loadingStore.startLoading();

    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    const loadingStore = useLoadingStore();
    loadingStore.stopLoading();
    return Promise.reject(error);
  }
);

// Auth endpoints that should NOT trigger token refresh
const AUTH_ENDPOINTS = [
  '/api/auth/login',
  '/api/auth/register',
  '/api/auth/forgot-password',
  '/api/auth/reset-password',
];

api.interceptors.response.use(
  (response) => {
    const loadingStore = useLoadingStore();
    loadingStore.stopLoading();
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    // Skip token refresh for auth endpoints - 401 here means invalid credentials, not expired token
    const isAuthEndpoint = AUTH_ENDPOINTS.some(endpoint => originalRequest.url?.includes(endpoint));

    if (error.response?.status === 401 && !originalRequest._retry && !isAuthEndpoint) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then(token => {
            originalRequest.headers.Authorization = `Bearer ${token}`;
            return api(originalRequest);
          })
          .catch(err => {
            return Promise.reject(err);
          });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        const response = await api.post('/api/auth/refresh');
        const { access_token } = response.data;

        localStorage.setItem('accessToken', access_token);
        api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;

        processQueue(null, access_token);

        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return api(originalRequest);
      } catch (refreshError) {
        processQueue(refreshError, null);

        // Properly clear auth and user state using store methods
        try {
          const authStore = useAuthStore();
          const userStore = useUserStore();
          authStore.clearAuth();
          userStore.clearProfile();

          // Use router for navigation instead of window.location
          router.push({ name: 'Login' });
        } catch (storeError) {
          // Fallback if stores aren't available (edge case on initial load)
          localStorage.removeItem('accessToken');
          window.location.href = '/login';
        }

        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    const loadingStore = useLoadingStore();
    loadingStore.stopLoading();

    // Show toast notification for errors (except 401 which is handled above)
    if (error.response?.status !== 401) {
      const toastStore = useToastStore();
      const message = getErrorMessage(error);
      toastStore.error(message);
    }

    return Promise.reject(error);
  }
);

export default api;
