<template>
  <div class="max-w-lg w-full">
    <form @submit.prevent="handleSubmit" class="flex flex-col gap-6">
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <BaseInput
          id="firstName"
          v-model="formData.firstName"
          type="text"
          label="First Name"
          placeholder="John"
          :disabled="loading"
          :error="errors.firstName"
          required
        />

        <BaseInput
          id="lastName"
          v-model="formData.lastName"
          type="text"
          label="Last Name"
          placeholder="Doe"
          :disabled="loading"
          :error="errors.lastName"
          required
        />
      </div>

      <BaseInput
        id="email"
        v-model="formData.email"
        type="email"
        label="Email"
        placeholder="john.doe@example.com"
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
        help-text="Minimum 8 characters, at least 1 uppercase letter and 1 number"
        required
      />

      <BaseInput
        id="confirmPassword"
        v-model="formData.confirmPassword"
        type="password"
        label="Confirm Password"
        placeholder="Confirm your password"
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
        {{ loading ? 'Registering...' : 'Register' }}
      </BaseButton>
    </form>

    <div class="mt-4 text-center">
      <router-link to="/login" class="text-blue-500 no-underline text-sm hover:underline">
        Already have an account? Login
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useAuth } from '../composables/useAuth';
import { BaseInput, BaseButton, BaseAlert } from './ui';

const { register, loading } = useAuth();

const formData = reactive({
  firstName: '',
  lastName: '',
  email: '',
  password: '',
  confirmPassword: '',
});

const errors = reactive({
  firstName: '',
  lastName: '',
  email: '',
  password: '',
  confirmPassword: '',
});

const errorMessage = ref('');
const successMessage = ref('');

function validateForm() {
  errors.firstName = '';
  errors.lastName = '';
  errors.email = '';
  errors.password = '';
  errors.confirmPassword = '';

  if (!formData.firstName.trim()) {
    errors.firstName = 'First name is required';
    return false;
  }

  if (!formData.lastName.trim()) {
    errors.lastName = 'Last name is required';
    return false;
  }

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

  try {
    await register(formData.email, formData.password, formData.firstName, formData.lastName);
    successMessage.value = 'Registration successful! Please login to continue.';
    formData.firstName = '';
    formData.lastName = '';
    formData.email = '';
    formData.password = '';
    formData.confirmPassword = '';
  } catch (err) {
    errorMessage.value = typeof err === 'string' ? err : 'Registration failed. Please try again.';
  }
}
</script>
