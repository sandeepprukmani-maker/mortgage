<template>
  <div class="max-w-md w-full">
    <form @submit.prevent="handleSubmit" class="flex flex-col gap-6">
      <BaseInput
        id="email"
        v-model="formData.email"
        type="email"
        label="Email"
        placeholder="Enter your email"
        :disabled="loading"
        :error="errors.email"
        required
      />

      <BaseInput
        id="password"
        v-model="formData.password"
        type="password"
        label="Password"
        placeholder="Enter your password"
        :disabled="loading"
        :error="errors.password"
        required
      />

      <BaseAlert v-if="errorMessage" variant="error">
        {{ errorMessage }}
      </BaseAlert>

      <BaseButton type="submit" variant="primary" :disabled="loading" :loading="loading">
        {{ loading ? 'Logging in...' : 'Login' }}
      </BaseButton>
    </form>

    <div class="mt-4 flex flex-col gap-2 text-center">
      <router-link to="/forgot-password" class="text-blue-500 no-underline text-sm hover:underline">
        Forgot password?
      </router-link>
      <router-link to="/register" class="text-blue-500 no-underline text-sm hover:underline">
        Don't have an account? Register
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '../composables/useAuth';
import { BaseInput, BaseButton, BaseAlert } from './ui';

const router = useRouter();
const { login, loading, error } = useAuth();

const formData = reactive({
  email: '',
  password: '',
});

const errors = reactive({
  email: '',
  password: '',
});

const errorMessage = ref('');

function validateForm() {
  errors.email = '';
  errors.password = '';

  if (!formData.email) {
    errors.email = 'Email is required';
    return false;
  }

  if (!/\S+@\S+\.\S+/.test(formData.email)) {
    errors.email = 'Email is invalid';
    return false;
  }

  if (!formData.password) {
    errors.password = 'Password is required';
    return false;
  }

  return true;
}

async function handleSubmit() {
  errorMessage.value = '';

  if (!validateForm()) {
    return;
  }

  try {
    await login(formData.email, formData.password);
    router.push('/dashboard');
  } catch (err) {
    errorMessage.value = typeof err === 'string' ? err : 'Invalid email or password';
  }
}
</script>
