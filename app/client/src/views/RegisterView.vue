<template>
  <section class="auth bg-base d-flex flex-wrap">
    <div class="auth-left d-lg-block d-none">
      <div class="d-flex align-items-center flex-column h-100 justify-content-center">
        <img src="@/assets/images/auth/auth-img.png" alt="Register illustration">
      </div>
    </div>
    <div class="auth-right py-32 px-24 d-flex flex-column justify-content-center">
      <div class="max-w-464-px mx-auto w-full">
        <div>
          <router-link to="/" class="mb-40 max-w-290-px d-block">
            <img src="@/assets/images/logo.png" alt="Valargen Logo">
          </router-link>
          <h4 class="mb-12 text-2xl font-semibold text-neutral-900">Sign Up to your Account</h4>
          <p class="mb-32 text-secondary-light text-lg">Welcome! Please enter your details</p>
        </div>
        <form @submit.prevent="handleSubmit">
          <!-- First Name & Last Name Row -->
          <div class="d-flex gap-3 mb-16">
            <div class="icon-field w-50">
              <span class="icon top-50 translate-middle-y">
                <Icon icon="f7:person" />
              </span>
              <input
                type="text"
                class="form-control h-56-px bg-neutral-50 radius-12"
                placeholder="First Name"
                v-model="formData.firstName"
                :disabled="loading"
                required
              >
            </div>
            <div class="icon-field w-50">
              <span class="icon top-50 translate-middle-y">
                <Icon icon="f7:person" />
              </span>
              <input
                type="text"
                class="form-control h-56-px bg-neutral-50 radius-12"
                placeholder="Last Name"
                v-model="formData.lastName"
                :disabled="loading"
                required
              >
            </div>
          </div>

          <!-- Email Input -->
          <div class="icon-field mb-16">
            <span class="icon top-50 translate-middle-y">
              <Icon icon="mage:email" />
            </span>
            <input
              type="email"
              class="form-control h-56-px bg-neutral-50 radius-12"
              placeholder="Email"
              v-model="formData.email"
              :disabled="loading"
              required
            >
          </div>

          <!-- Password Input -->
          <div class="position-relative mb-16">
            <div class="icon-field">
              <span class="icon top-50 translate-middle-y">
                <Icon icon="solar:lock-password-outline" />
              </span>
              <input
                :type="showPassword ? 'text' : 'password'"
                class="form-control h-56-px bg-neutral-50 radius-12"
                placeholder="Password"
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
                placeholder="Confirm Password"
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

          <!-- Terms & Conditions -->
          <div class="d-flex justify-content-between gap-2">
            <div class="form-check style-check d-flex align-items-start">
              <input
                class="form-check-input border mt-4"
                type="checkbox"
                v-model="formData.termsAccepted"
                id="terms"
              >
              <label class="form-check-label text-sm" for="terms">
                By creating an account you agree to the
                <a href="#" class="text-primary-600 fw-semibold">Terms & Conditions</a> and our
                <a href="#" class="text-primary-600 fw-semibold">Privacy Policy</a>
              </label>
            </div>
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
            {{ loading ? 'Signing up...' : 'Sign Up' }}
          </button>

          <!-- Divider -->
          <div class="mt-32 center-border-horizontal text-center">
            <span class="bg-base z-1 px-4 text-sm text-secondary-light">Or sign up with</span>
          </div>

          <!-- Social Login Buttons -->
          <div class="mt-32 d-flex align-items-center gap-3">
            <button
              type="button"
              class="fw-semibold text-primary-light py-16 px-24 w-50 border radius-12 text-md d-flex align-items-center justify-content-center gap-12 line-height-1 bg-hover-primary-50"
              disabled
            >
              <Icon icon="ic:baseline-facebook" class="text-primary-600 text-xl line-height-1" />
              Facebook
            </button>
            <button
              type="button"
              class="fw-semibold text-primary-light py-16 px-24 w-50 border radius-12 text-md d-flex align-items-center justify-content-center gap-12 line-height-1 bg-hover-primary-50"
              @click="handleGoogleLogin"
              :disabled="googleLoading"
            >
              <Icon icon="logos:google-icon" class="text-xl line-height-1" />
              {{ googleLoading ? 'Loading...' : 'Google' }}
            </button>
          </div>

          <!-- Sign In Link -->
          <div class="mt-32 text-center text-sm">
            <p class="mb-0 text-secondary-light">Already have an account? <router-link to="/login" class="text-primary-600 fw-semibold">Sign In</router-link></p>
          </div>
        </form>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useAuth } from '../composables/useAuth';
import { useGoogleAuth } from '../composables/useGoogleAuth';

const { register, loading } = useAuth();
const { loginWithGoogle, loading: googleLoading } = useGoogleAuth();

const formData = reactive({
  firstName: '',
  lastName: '',
  email: '',
  password: '',
  confirmPassword: '',
  termsAccepted: false,
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
  if (!formData.firstName.trim()) {
    errorMessage.value = 'First name is required';
    return false;
  }

  if (!formData.lastName.trim()) {
    errorMessage.value = 'Last name is required';
    return false;
  }

  if (!formData.email) {
    errorMessage.value = 'Email is required';
    return false;
  }

  if (!/\S+@\S+\.\S+/.test(formData.email)) {
    errorMessage.value = 'Please enter a valid email';
    return false;
  }

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

  if (!formData.termsAccepted) {
    errorMessage.value = 'You must accept the terms and conditions';
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
    formData.termsAccepted = false;
  } catch (err) {
    errorMessage.value = typeof err === 'string' ? err : 'Registration failed. Please try again.';
  }
}

function handleGoogleLogin() {
  loginWithGoogle();
}
</script>

<style scoped>
.w-full {
  width: 100%;
}

.px-4 {
  padding-left: 1rem;
  padding-right: 1rem;
}

.z-1 {
  position: relative;
  z-index: 1;
}
</style>
