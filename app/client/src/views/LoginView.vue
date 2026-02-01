<template>
  <section class="auth bg-base d-flex flex-wrap">
    <div class="auth-left d-lg-block d-none">
      <div class="d-flex align-items-center flex-column h-100 justify-content-center">
        <img src="@/assets/images/auth/auth-img.png" alt="Login illustration">
      </div>
    </div>
    <div class="auth-right py-32 px-24 d-flex flex-column justify-content-center">
      <div class="max-w-464-px mx-auto w-full">
        <div>
          <router-link to="/" class="mb-40 max-w-290-px d-block">
            <img src="@/assets/images/logo.png" alt="Valargen Logo">
          </router-link>
          <h4 class="mb-12 text-2xl font-semibold text-neutral-900">Sign In to your Account</h4>
          <p class="mb-32 text-secondary-light text-lg">Welcome back! Please enter your details</p>
        </div>
        <form @submit.prevent="handleSubmit">
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
          <div class="position-relative mb-20">
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

          <!-- Remember Me & Forgot Password -->
          <div class="d-flex justify-content-between gap-2">
            <div class="form-check style-check d-flex align-items-center">
              <input
                class="form-check-input border"
                type="checkbox"
                id="remember"
                v-model="rememberMe"
              >
              <label class="form-check-label text-sm" for="remember">Remember me</label>
            </div>
            <router-link to="/forgot-password" class="text-primary-600 fw-medium text-sm">Forgot Password?</router-link>
          </div>

          <!-- Error Message -->
          <div v-if="errorMessage" class="alert alert-danger mt-16 text-sm">
            {{ errorMessage }}
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            class="btn btn-primary text-sm btn-sm px-12 py-16 w-full radius-12 mt-32"
            :disabled="loading"
          >
            {{ loading ? 'Signing in...' : 'Sign In' }}
          </button>

          <!-- Divider -->
          <div class="mt-32 center-border-horizontal text-center">
            <span class="bg-base z-1 px-4 text-sm text-secondary-light">Or sign in with</span>
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

          <!-- Sign Up Link -->
          <div class="mt-32 text-center text-sm">
            <p class="mb-0 text-secondary-light">Don't have an account? <router-link to="/register" class="text-primary-600 fw-semibold">Sign Up</router-link></p>
          </div>
        </form>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '../composables/useAuth';
import { useGoogleAuth } from '../composables/useGoogleAuth';

const router = useRouter();
const { login, loading } = useAuth();
const { loginWithGoogle, loading: googleLoading } = useGoogleAuth();

const formData = reactive({
  email: '',
  password: '',
});

const showPassword = ref(false);
const rememberMe = ref(false);
const errorMessage = ref('');

function togglePassword() {
  showPassword.value = !showPassword.value;
}

async function handleSubmit() {
  errorMessage.value = '';

  if (!formData.email) {
    errorMessage.value = 'Email is required';
    return;
  }

  if (!/\S+@\S+\.\S+/.test(formData.email)) {
    errorMessage.value = 'Please enter a valid email';
    return;
  }

  if (!formData.password) {
    errorMessage.value = 'Password is required';
    return;
  }

  try {
    await login(formData.email, formData.password);
    router.push('/dashboard');
  } catch (err) {
    errorMessage.value = typeof err === 'string' ? err : 'Invalid email or password';
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
