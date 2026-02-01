<template>
  <div class="max-w-md w-full">
    <form @submit.prevent="handleSubmit" class="flex flex-col gap-6">
      <BaseInput
        id="password"
        v-model="formData.password"
        type="password"
        label="New Password"
        placeholder="Enter your new password"
        :disabled="loading"
        :error="errors.password"
        help-text="Minimum 8 characters, at least 1 uppercase letter and 1 number"
        required
      />

      <BaseInput
        id="confirmPassword"
        v-model="formData.confirmPassword"
        type="password"
        label="Confirm New Password"
        placeholder="Confirm your new password"
        :disabled="loading"
        :error="errors.confirmPassword"
        required
      />

      <BaseAlert v-if="errorMessage" variant="error">
        {{ errorMessage }}
      </BaseAlert>

      <BaseAlert v-if="successMessage" variant="success">
        {{ successMessage }}
      </BaseAlert>

      <BaseButton type="submit" variant="primary" :disabled="loading || !!successMessage" :loading="loading">
        {{ loading ? 'Resetting...' : 'Reset Password' }}
      </BaseButton>
    </form>

    <div class="mt-4 text-center">
      <router-link to="/login" class="text-blue-500 no-underline text-sm hover:underline">
        Back to Login
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuth } from '../composables/useAuth';
import { BaseInput, BaseButton, BaseAlert } from './ui';

const router = useRouter();
const route = useRoute();
const { resetPassword, loading } = useAuth();

const formData = reactive({
  password: '',
  confirmPassword: '',
});

const errors = reactive({
  password: '',
  confirmPassword: '',
});

const errorMessage = ref('');
const successMessage = ref('');

function validateForm() {
  errors.password = '';
  errors.confirmPassword = '';

  if (!formData.password) {
    errors.password = 'Password is required';
    return false;
  }

  if (formData.password.length < 8) {
    errors.password = 'Password must be at least 8 characters';
    return false;
  }

  if (!/[A-Z]/.test(formData.password)) {
    errors.password = 'Password must contain at least 1 uppercase letter';
    return false;
  }

  if (!/[0-9]/.test(formData.password)) {
    errors.password = 'Password must contain at least 1 number';
    return false;
  }

  if (!formData.confirmPassword) {
    errors.confirmPassword = 'Please confirm your password';
    return false;
  }

  if (formData.password !== formData.confirmPassword) {
    errors.confirmPassword = 'Passwords do not match';
    return false;
  }

  return true;
}

async function handleSubmit() {
  errorMessage.value = '';
  successMessage.value = '';

  if (!validateForm()) {
    return;
  }

  const token = route.params.token;

  if (!token) {
    errorMessage.value = 'Invalid reset token';
    return;
  }

  try {
    await resetPassword(token, formData.password);
    successMessage.value = 'Password reset successful! Redirecting to login...';
    setTimeout(() => {
      router.push('/login');
    }, 2000);
  } catch (err) {
    errorMessage.value = typeof err === 'string' ? err : 'Password reset failed. The token may be invalid or expired.';
  }
}
</script>
