import { defineStore } from 'pinia';
import { ref } from 'vue';
import { userService } from '../services/userService';

export const useUserStore = defineStore('user', () => {
  const profile = ref(null);
  const loading = ref(false);
  const error = ref(null);

  async function fetchProfile() {
    loading.value = true;
    error.value = null;
    try {
      profile.value = await userService.getCurrentUser();
      return profile.value;
    } catch (err) {
      error.value = err;
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function updateProfile(data) {
    loading.value = true;
    error.value = null;
    try {
      profile.value = await userService.updateProfile(data);
      return profile.value;
    } catch (err) {
      error.value = err;
      throw err;
    } finally {
      loading.value = false;
    }
  }

  function clearProfile() {
    profile.value = null;
    error.value = null;
  }

  return {
    profile,
    loading,
    error,
    fetchProfile,
    updateProfile,
    clearProfile,
  };
});
