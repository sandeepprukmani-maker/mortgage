<template>
  <div id="app" class="min-h-screen">
    <LoadingIndicator />
    <ToastNotification />
    <router-view />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useAuthStore } from './stores/auth';
import { useUserStore } from './stores/user';
import { useThemeStore } from './stores/theme';
import LoadingIndicator from './components/ui/LoadingIndicator.vue';
import ToastNotification from './components/ui/ToastNotification.vue';

const authStore = useAuthStore();
const userStore = useUserStore();
const themeStore = useThemeStore();

onMounted(async () => {
  themeStore.initTheme();
  const hasAuth = authStore.checkAuth();

  // Fetch user profile if authenticated
  if (hasAuth) {
    try {
      await userStore.fetchProfile();
    } catch (error) {
      // If profile fetch fails (e.g., token expired), auth will handle redirect
      console.error('Failed to fetch user profile:', error);
    }
  }
});
</script>
