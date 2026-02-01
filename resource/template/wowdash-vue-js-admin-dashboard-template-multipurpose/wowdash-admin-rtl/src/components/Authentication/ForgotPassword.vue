<template>
    <section class="auth forgot-password-page bg-base d-flex flex-wrap">
      <div class="auth-left d-lg-block d-none">
        <div class="d-flex align-items-center flex-column h-100 justify-content-center">
          <img src="@/assets/images/auth/forgot-pass-img.png" alt="">
        </div>
      </div>
      <div class="auth-right py-32 px-24 d-flex flex-column justify-content-center">
        <div class="max-w-464-px mx-auto w-100">
          <div>
            <h4 class="mb-12">Forgot Password</h4>
            <p class="mb-32 text-secondary-light text-lg">
              Enter the email address associated with your account and we will send you a link to reset your password.
            </p>
          </div>
          <form @submit.prevent="openModal">
            <div class="icon-field">
              <span class="icon top-50 translate-middle-y">
                <iconify-icon icon="mage:email"></iconify-icon>
              </span>
              <input type="email" v-model="email" class="form-control h-56-px bg-neutral-50 radius-12" placeholder="Enter Email" required>
            </div>
            <button type="submit" class="btn btn-primary text-sm btn-sm px-12 py-16 w-100 radius-12 mt-32">
              Continue
            </button>
  
            <div class="text-center">
              <router-link to="sign-in" class="text-primary-600 fw-bold mt-24">Back to Sign In</router-link>
            </div>
  
            <div class="mt-120 text-center text-sm">
              <p class="mb-0">Already have an account? <router-link to="/sign-in" class="text-primary-600 fw-semibold">Sign In</router-link></p>
            </div>
          </form>
        </div>
      </div>
  
      <!-- Modal -->
      <div class="modal fade" id="exampleModal" ref="emailModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog modal-dialog-centered">
          <div class="modal-content radius-16 bg-base">
            <div class="modal-body p-40 text-center">
              <div class="mb-32">
                <img src="@/assets/images/auth/envelop-icon.png" alt="">
              </div>
              <h6 class="mb-12">Verify your Email</h6>
              <p class="text-secondary-light text-sm mb-0">
                Thank you, check your email for instructions to reset your password
              </p>
              <button type="button" class="btn btn-primary text-sm btn-sm px-12 py-16 w-100 radius-12 mt-32" data-bs-dismiss="modal">
                Skip
              </button>
              <div class="mt-32 text-sm">
                <p class="mb-0">
                  Don’t receive an email?
                  <router-link to="/resend" class="text-primary-600 fw-semibold">Resend</router-link>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </template>
  
  <script>
  export default {
    name: 'ForgotPassword',
    data() {
      return {
        email: ''
      };
    },
    methods: {
      openModal() {
        const modal = new bootstrap.Modal(this.$refs.emailModal);
        modal.show();
      }
    }
  };
  </script>
  