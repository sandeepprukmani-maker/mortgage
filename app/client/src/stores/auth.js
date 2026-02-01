import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref(localStorage.getItem('accessToken') || null);
  const user = ref(null);

  const isAuthenticated = computed(() => !!accessToken.value);

  function setAuth(token, userData) {
    accessToken.value = token;
    user.value = userData;
    localStorage.setItem('accessToken', token);
  }

  function setToken(token) {
    accessToken.value = token;
    localStorage.setItem('accessToken', token);
  }

  function clearAuth() {
    accessToken.value = null;
    user.value = null;
    localStorage.removeItem('accessToken');
  }

  function checkAuth() {
    const token = localStorage.getItem('accessToken');
    if (token) {
      accessToken.value = token;
      return true;
    }
    return false;
  }

  return {
    accessToken,
    user,
    isAuthenticated,
    setAuth,
    setToken,
    clearAuth,
    checkAuth,
  };
});
