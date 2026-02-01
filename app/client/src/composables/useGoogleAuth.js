import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { useUserStore } from '../stores/user';
import { authService } from '../services/authService';

export function useGoogleAuth() {
  const router = useRouter();
  const authStore = useAuthStore();
  const userStore = useUserStore();

  const loading = ref(false);
  const error = ref(null);

  async function loginWithGoogle() {
    loading.value = true;
    error.value = null;
    try {
      const data = await authService.getGoogleAuthUrl();
      window.location.href = data.authorization_url;
    } catch (err) {
      error.value = err;
      loading.value = false;
      throw err;
    }
  }

  async function handleGoogleCallback(code) {
    loading.value = true;
    error.value = null;
    try {
      const response = await authService.login(code, null);
      authStore.setAuth(response.access_token, response.user);
      await userStore.fetchProfile();
      router.push('/dashboard');
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
    loginWithGoogle,
    handleGoogleCallback,
  };
}
