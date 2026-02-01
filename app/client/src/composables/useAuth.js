import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { useUserStore } from '../stores/user';
import { authService } from '../services/authService';

export function useAuth() {
  const router = useRouter();
  const authStore = useAuthStore();
  const userStore = useUserStore();

  const loading = ref(false);
  const error = ref(null);

  const isAuthenticated = computed(() => authStore.isAuthenticated);
  const user = computed(() => authStore.user);

  async function login(email, password) {
    loading.value = true;
    error.value = null;
    try {
      const data = await authService.login(email, password);
      authStore.setAuth(data.access_token, data.user);
      await userStore.fetchProfile();
      return data;
    } catch (err) {
      error.value = err;
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function register(email, password, firstName, lastName) {
    loading.value = true;
    error.value = null;
    try {
      const data = await authService.register(email, password, firstName, lastName);
      return data;
    } catch (err) {
      error.value = err;
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function logout() {
    loading.value = true;
    error.value = null;
    try {
      await authService.logout();
      authStore.clearAuth();
      userStore.clearProfile();
      router.push('/login');
    } catch (err) {
      error.value = err;
      authStore.clearAuth();
      userStore.clearProfile();
      router.push('/login');
    } finally {
      loading.value = false;
    }
  }

  async function forgotPassword(email) {
    loading.value = true;
    error.value = null;
    try {
      const data = await authService.forgotPassword(email);
      return data;
    } catch (err) {
      error.value = err;
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function resetPassword(token, newPassword) {
    loading.value = true;
    error.value = null;
    try {
      const data = await authService.resetPassword(token, newPassword);
      return data;
    } catch (err) {
      error.value = err;
      throw err;
    } finally {
      loading.value = false;
    }
  }

  return {
    loading,
    error,
    isAuthenticated,
    user,
    login,
    register,
    logout,
    forgotPassword,
    resetPassword,
  };
}
