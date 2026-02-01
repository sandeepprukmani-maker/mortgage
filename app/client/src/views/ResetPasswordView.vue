<template>
  <section class="auth forgot-password-page bg-base d-flex flex-wrap">
    <div class="auth-left d-lg-block d-none">
      <div class="d-flex align-items-center flex-column h-100 justify-content-center">
        <img src="@/assets/images/auth/forgot-pass-img.png" alt="Reset password illustration">
      </div>
    </div>
    <div class="auth-right py-32 px-24 d-flex flex-column justify-content-center">
      <div class="max-w-464-px mx-auto w-full">
        <div>
          <h4 class="mb-12 text-2xl font-semibold text-neutral-900">Reset Password</h4>
          <p class="mb-32 text-secondary-light text-lg">Enter your new password below</p>
        </div>
        <form @submit.prevent="handleSubmit">
          <!-- New Password Input -->
          <div class="position-relative mb-16">
            <div class="icon-field">
              <span class="icon top-50 translate-middle-y">
                <Icon icon="solar:lock-password-outline" />
              </span>
              <input
                :type="showPassword ? 'text' : 'password'"
                class="form-control h-56-px bg-neutral-50 radius-12"
                placeholder="New Password"
                v-model="formData.password"
                :disabled="loading"
                required
              >
            </div>
            <span
              class="toggle-password cursor-pointer position-absolute end-0 top-50 translate-middle-y me-16 text-secondary-light"
              @click="togglePassword"
            >
              <Icon :icon="showPassword ? 'ri:eye-off-line' : 'ri:eye-line'" />
            </span>
          </div>

          <!-- Confirm Password Input -->
          <div class="position-relative mb-20">
            <div class="icon-field">
              <span class="icon top-50 translate-middle-y">
                <Icon icon="solar:lock-password-outline" />
              </span>
              <input
                :type="showConfirmPassword ? 'text' : 'password'"
                class="form-control h-56-px bg-neutral-50 radius-12"
                placeholder="Confirm New Password"
                v-model="formData.confirmPassword"
                :disabled="loading"
                required
              >
            </div>
            <span
              class="toggle-password cursor-pointer position-absolute end-0 top-50 translate-middle-y me-16 text-secondary-light"
              @click="toggleConfirmPassword"
            >
              <Icon :icon="showConfirmPassword ? 'ri:eye-off-line' : 'ri:eye-line'" />
            </span>
          </div>

          <!-- Password Requirements -->
          <span class="text-sm text-secondary-light mb-16 d-block">
            Password must have at least 8 characters, 1 uppercase letter, and 1 number
          </span>

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
            {{ loading ? 'Resetting...' : 'Reset Password' }}
          </button>

          <!-- Back to Sign In -->
          <div class="text-center mt-32">
            <router-link to="/login" class="text-primary-600 fw-bold">Back to Sign In</router-link>
          </div>
        </form>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuth } from '../composables/useAuth';

const router = useRouter();
const route = useRoute();
const { resetPassword, loading } = useAuth();

const formData = reactive({
  password: '',
  confirmPassword: '',
});

const showPassword = ref(false);
const showConfirmPassword = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

function togglePassword() {
  showPassword.value = !showPassword.value;
}

function toggleConfirmPassword() {
  showConfirmPassword.value = !showConfirmPassword.value;
}

function validateForm() {
  if (!formData.password) {
    errorMessage.value = 'Password is required';
    return false;
  }

  if (formData.password.length < 8) {
    errorMessage.value = 'Password must be at least 8 characters';
    return false;
  }

  if (!/[A-Z]/.test(formData.password)) {
    errorMessage.value = 'Password must contain at least 1 uppercase letter';
    return false;
  }

  if (!/[0-9]/.test(formData.password)) {
    errorMessage.value = 'Password must contain at least 1 number';
    return false;
  }

  if (!formData.confirmPassword) {
    errorMessage.value = 'Please confirm your password';
    return false;
  }

  if (formData.password !== formData.confirmPassword) {
    errorMessage.value = 'Passwords do not match';
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

<style scoped>
.w-full {
  width: 100%;
}
</style>
