<template>
  <div class="max-w-md w-full">
    <form @submit.prevent="handleSubmit" class="flex flex-col gap-6">
      <BaseInput
        id="email"
        v-model="formData.email"
        type="email"
        label="Email"
        placeholder="Enter your email"
        :disabled="loading || !!successMessage"
        :error="errors.email"
        required
      />

      <BaseAlert v-if="errorMessage" variant="error">
        {{ errorMessage }}
      </BaseAlert>

      <BaseAlert v-if="successMessage" variant="success">
        {{ successMessage }}
      </BaseAlert>

      <BaseButton type="submit" variant="primary" :disabled="loading || !!successMessage" :loading="loading">
        {{ loading ? 'Sending...' : 'Send Reset Link' }}
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
import { useAuth } from '../composables/useAuth';
import { BaseInput, BaseButton, BaseAlert } from './ui';

const { forgotPassword, loading } = useAuth();

const formData = reactive({
  email: '',
});

const errors = reactive({
  email: '',
});

const errorMessage = ref('');
const successMessage = ref('');

function validateForm() {
  errors.email = '';

  if (!formData.email) {
    errors.email = 'Email is required';
    return false;
  }

  if (!/\S+@\S+\.\S+/.test(formData.email)) {
    errors.email = 'Email is invalid';
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

  try {
    await forgotPassword(formData.email);
    successMessage.value = 'If an account exists with this email, you will receive a password reset link shortly. Please check your console logs (MVP mode).';
  } catch (err) {
    successMessage.value = 'If an account exists with this email, you will receive a password reset link shortly.';
  }
}
</script>
