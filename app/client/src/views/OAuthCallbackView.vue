<template>
  <div class="flex justify-center items-center min-h-screen bg-gray-100">
    <div v-if="loading" class="text-center p-8 bg-white rounded-lg shadow-card">
      <div class="w-10 h-10 mx-auto mb-4 border-[3px] border-gray-200 border-t-blue-500 rounded-full animate-spin"></div>
      <p class="text-gray-600">Completing sign in...</p>
    </div>
    <div v-else-if="error" class="text-center p-8 bg-white rounded-lg shadow-card max-w-md">
      <div class="text-red-600 mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mx-auto">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="12"></line>
          <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
      </div>
      <h2 class="m-0 mb-2 text-xl font-semibold text-gray-800">Sign-in Failed</h2>
      <p class="m-0 mb-4 text-red-600 text-sm leading-relaxed">{{ error }}</p>
      <p v-if="isConfigError" class="m-0 mb-4 p-3 bg-yellow-100 rounded text-yellow-800 text-sm">
        If this problem persists, please contact your administrator.
      </p>
      <router-link
        to="/login"
        class="inline-block px-4 py-2 bg-blue-500 text-white no-underline rounded font-medium transition-colors duration-200 hover:bg-blue-600"
      >
        Back to Login
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { useUserStore } from '../stores/user';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const userStore = useUserStore();

const loading = ref(true);
const error = ref(null);

// Check if the error is a configuration error that requires admin attention
const isConfigError = computed(() => {
  if (!error.value) return false;
  const configKeywords = [
    'not configured',
    'credentials',
    'GOOGLE_CLIENT',
    'redirect URI mismatch',
    'not available'
  ];
  return configKeywords.some(keyword =>
    error.value.toLowerCase().includes(keyword.toLowerCase())
  );
});

onMounted(async () => {
  const accessToken = route.query.access_token;
  const errorParam = route.query.error;

  if (errorParam) {
    error.value = errorParam;
    loading.value = false;
    return;
  }

  if (!accessToken) {
    error.value = 'No access token received. Please try signing in again.';
    loading.value = false;
    return;
  }

  try {
    // Store the token
    authStore.setToken(accessToken);

    // Fetch user profile
    await userStore.fetchProfile();

    // Redirect to dashboard
    router.push('/dashboard');
  } catch (err) {
    console.error('OAuth callback error:', err);
    error.value = err.message || 'Failed to complete sign in. Please try again.';
    authStore.clearAuth();
    loading.value = false;
  }
});
</script>
