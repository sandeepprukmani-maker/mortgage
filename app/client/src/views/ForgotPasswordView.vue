<template>
  <section class="auth forgot-password-page bg-base d-flex flex-wrap">
    <div class="auth-left d-lg-block d-none">
      <div class="d-flex align-items-center flex-column h-100 justify-content-center">
        <img src="@/assets/images/auth/forgot-pass-img.png" alt="Forgot password illustration">
      </div>
    </div>
    <div class="auth-right py-32 px-24 d-flex flex-column justify-content-center">
      <div class="max-w-464-px mx-auto w-full">
        <div>
          <h4 class="mb-12 text-2xl font-semibold text-neutral-900">Forgot Password</h4>
          <p class="mb-32 text-secondary-light text-lg">
            Enter the email address associated with your account and we will send you a link to reset your password.
          </p>
        </div>
        <form @submit.prevent="handleSubmit">
          <!-- Email Input -->
          <div class="icon-field">
            <span class="icon top-50 translate-middle-y">
              <Icon icon="mage:email" />
            </span>
            <input
              type="email"
              class="form-control h-56-px bg-neutral-50 radius-12"
              placeholder="Enter Email"
              v-model="email"
              :disabled="loading || !!successMessage"
              required
            >
          </div>

          <!-- Error Message -->
          <div v-if="errorMessage" class="alert alert-danger mt-16 text-sm">
            {{ errorMessage }}
          </div>

          <!-- Success Message -->
          <div v-if="successMessage" class="alert alert-success mt-16 text-sm">
            {{ successMessage }}
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            class="btn btn-primary text-sm btn-sm px-12 py-16 w-full radius-12 mt-32"
            :disabled="loading || !!successMessage"
          >
            {{ loading ? 'Sending...' : 'Continue' }}
          </button>

          <!-- Back to Sign In -->
          <div class="text-center mt-32">
            <router-link to="/login" class="text-primary-600 fw-bold">Back to Sign In</router-link>
          </div>

          <!-- Sign In Link -->
          <div class="mt-120 text-center text-sm">
            <p class="mb-0 text-secondary-light">Already have an account? <router-link to="/login" class="text-primary-600 fw-semibold">Sign In</router-link></p>
          </div>
        </form>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue';
import { useAuth } from '../composables/useAuth';

const { forgotPassword, loading } = useAuth();

const email = ref('');
const errorMessage = ref('');
const successMessage = ref('');

async function handleSubmit() {
  errorMessage.value = '';
  successMessage.value = '';

  if (!email.value) {
    errorMessage.value = 'Email is required';
    return;
  }

  if (!/\S+@\S+\.\S+/.test(email.value)) {
    errorMessage.value = 'Please enter a valid email';
    return;
  }

  try {
    await forgotPassword(email.value);
    successMessage.value = 'If an account exists with this email, you will receive a password reset link shortly. Please check your console logs (MVP mode).';
  } catch (err) {
    successMessage.value = 'If an account exists with this email, you will receive a password reset link shortly.';
  }
}
</script>

<style scoped>
.w-full {
  width: 100%;
}
</style>
