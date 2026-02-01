<template>
  <div class="col-md-6">
    <div class="card">
      <div class="card-body">
        <h6 class="mb-4 text-xl">Wizard with beside label</h6>
        <p class="text-neutral-500">Fill up your details and proceed next steps.</p>
        <div class="form-wizard">
          <form @submit.prevent>
            <div class="form-wizard-header overflow-x-auto scroll-sm pb-8 my-32">
              <ul class="list-unstyled form-wizard-list style-three">
                <li v-for="(step, index) in steps" :key="index"
                  class="form-wizard-list__item d-flex align-items-center gap-8" :class="{
                    active: currentStep === index,
                    activated: currentStep > index
                  }">
                  <div class="form-wizard-list__line">
                    <span class="count">{{ index + 1 }}</span>
                  </div>
                  <span class="text text-xs fw-semibold">{{ step }}</span>
                </li>
              </ul>
            </div>

            <!-- Step 0 -->
            <div v-if="currentStep === 0" class="wizard-fieldset show">
              <h6 class="text-md text-neutral-500">Personal Information</h6>
              <div class="row gy-3">
                <div class="col-sm-6">
                  <label class="form-label">First Name*</label>
                  <input v-model="form.firstName" type="text" class="form-control wizard-required"
                    :class="{ 'border-danger': submitted && !form.firstName }" placeholder="Enter First Name"
                    required />
                </div>
                <div class="col-sm-6">
                  <label class="form-label">Last Name*</label>
                  <input v-model="form.lastName" type="text" class="form-control wizard-required"
                    :class="{ 'border-danger': submitted && !form.lastName }" placeholder="Enter Last Name" required />
                </div>
                <div class="col-12">
                  <label class="form-label">Email*</label>
                  <input v-model="form.email" type="email" class="form-control wizard-required"
                    :class="{ 'border-danger': submitted && !form.email }" placeholder="Enter Email" required />
                </div>
                <div class="col-sm-6">
                  <label class="form-label">Password*</label>
                  <input v-model="form.password" type="password" class="form-control wizard-required"
                    :class="{ 'border-danger': submitted && !form.password }" placeholder="Enter Password" required />
                </div>
                <div class="col-sm-6">
                  <label class="form-label">Confirm Password*</label>
                  <input v-model="form.confirmPassword" type="password" class="form-control wizard-required"
                    :class="{ 'border-danger': submitted && !form.confirmPassword }"
                    placeholder="Enter Confirm Password" required />
                </div>
                <div class="form-group text-end">
                  <button type="button" class="form-wizard-next-btn btn btn-primary-600 px-32"
                    @click="nextStep">Next</button>
                </div>
              </div>
            </div>

            <!-- Step 1 -->
            <div v-if="currentStep === 1" class="wizard-fieldset show">
              <h6 class="text-md text-neutral-500">Account Information</h6>
              <div class="row gy-3">
                <div class="col-12">
                  <label class="form-label">User Name*</label>
                  <input v-model="form.username" type="text" class="form-control wizard-required"
                    :class="{ 'border-danger': submitted && !form.username }" placeholder="Enter User Name" required />
                </div>
                <div class="col-sm-4">
                  <label class="form-label">Card Number*</label>
                  <input v-model="form.cardNumber" type="number" class="form-control wizard-required"
                    :class="{ 'border-danger': submitted && !form.cardNumber }" placeholder="Enter Card Number"
                    required />
                </div>
                <div class="col-sm-4">
                  <label class="form-label">Card Expiration(MM/YY)*</label>
                  <input v-model="form.cardExpiration" type="text" class="form-control wizard-required"
                    :class="{ 'border-danger': submitted && !form.cardExpiration }" placeholder="Enter Card Expiration"
                    required />
                </div>
                <div class="col-sm-4">
                  <label class="form-label">CVV Number*</label>
                  <input v-model="form.cardCVV" type="number" class="form-control wizard-required"
                    :class="{ 'border-danger': submitted && !form.cardCVV }" placeholder="CVV Number" required />
                </div>
                <div class="col-12">
                  <label class="form-label">Password*</label>
                  <input v-model="form.password" type="password" class="form-control wizard-required"
                    :class="{ 'border-danger': submitted && !form.password }" placeholder="Enter Password" required />
                </div>
                <div class="form-group d-flex align-items-center justify-content-end gap-8">
                  <button type="button" class="form-wizard-previous-btn btn btn-neutral-500 border-neutral-100 px-32"
                    @click="prevStep">Back</button>
                  <button type="button" class="form-wizard-next-btn btn btn-primary-600 px-32"
                    @click="nextStep">Next</button>
                </div>
              </div>
            </div>

            <!-- Step 2 -->
            <div v-if="currentStep === 2" class="wizard-fieldset show">
              <h6 class="text-md text-neutral-500">Bank Information</h6>
              <div class="row gy-3">
                <div class="col-sm-6">
                  <label class="form-label">Bank Name*</label>
                  <input v-model="form.bankName" type="text" class="form-control wizard-required"
                    :class="{ 'border-danger': submitted && !form.bankName }" placeholder="Enter Bank Name" required />
                </div>
                <div class="col-sm-6">
                  <label class="form-label">Branch Name*</label>
                  <input v-model="form.branchName" type="text" class="form-control wizard-required"
                    :class="{ 'border-danger': submitted && !form.branchName }" placeholder="Enter Branch Name"
                    required />
                </div>
                <div class="col-sm-6">
                  <label class="form-label">Account Name*</label>
                  <input v-model="form.accountName" type="text" class="form-control wizard-required"
                    :class="{ 'border-danger': submitted && !form.accountName }" placeholder="Enter Account Name"
                    required />
                </div>
                <div class="col-sm-6">
                  <label class="form-label">Account Number*</label>
                  <input v-model="form.accountNumber" type="number" class="form-control wizard-required"
                    :class="{ 'border-danger': submitted && !form.accountNumber }" placeholder="Enter Account Number"
                    required />
                </div>
                <div class="form-group d-flex align-items-center justify-content-end gap-8">
                  <button type="button" class="form-wizard-previous-btn btn btn-neutral-500 border-neutral-100 px-32"
                    @click="prevStep">Back</button>
                  <button type="button" class="form-wizard-next-btn btn btn-primary-600 px-32"
                    @click="nextStep">Next</button>
                </div>
              </div>
            </div>

            <!-- Final Step (Completion) -->
            <div v-if="currentStep === steps.length - 1" class="wizard-fieldset show">
              <div class="text-center mb-40">
                <img src="@/assets/images/gif/success-img3.gif" alt="" class="gif-image mb-24" />
                <h6 class="text-md text-neutral-600">Congratulations </h6>
                <p class="text-neutral-400 text-sm mb-0">Well done! You have successfully completed.</p>
              </div>
              <div class="form-group d-flex align-items-center justify-content-end gap-8">
                <button type="button" class="form-wizard-previous-btn btn btn-neutral-500 border-neutral-100 px-32"
                  @click="prevStep">Back</button>
                <button type="submit" class="form-wizard-submit btn btn-primary-600 px-32">Publish</button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      currentStep: 0,
      submitted: false,
      steps: [
        'Order Details',
        'Manufactures',
        'Order Plan',
        'Completed'
      ],
      form: {
        // Step 0
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        confirmPassword: '',

        // Step 1
        username: '',
        accountCardNumber: '',
        cardExpiration: '',
        cardCVV: '',
        accountPassword: '',

        // Step 2
        bankName: '',
        branchName: '',
        accountName: '',
        accountNumber: '',
      }
    };
  },
  methods: {
    nextStep() {
      this.submitted = true;

      const stepFields = {
        0: ['firstName', 'lastName', 'email', 'password', 'confirmPassword'],
        1: ['username', 'cardNumber', 'cardExpiration', 'cardCVV', 'password'],
        2: ['bankName', 'branchName', 'accountName', 'accountNumber'],
      };

      const requiredFields = stepFields[this.currentStep] || [];
      const isValid = requiredFields.every(field => !!this.form[field]);

      if (isValid && this.currentStep < this.steps.length - 1) {
        this.currentStep++;
        this.submitted = false;
      }
    },

    prevStep() {
      if (this.currentStep > 0) {
        this.currentStep--;
      }
    }
  }
};
</script>

<style scoped>
.form-wizard-list__item.active .count {
  color: #007bff;
}

.border-danger {
  border: 1px solid #ef4a00 !important;
  box-shadow: none !important;
}
</style>
