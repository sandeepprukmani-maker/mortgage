<template>
    <div class="card h-100 p-0 radius-12">
      <div class="card-body p-24">
        <div class="row gy-4">
          <!-- Paypal Section -->
          <div class="col-xxl-6">
            <div class="card radius-12 shadow-none border overflow-hidden">
              <div class="card-header bg-neutral-100 border-bottom py-16 px-24 d-flex align-items-center flex-wrap gap-3 justify-content-between">
                <div class="d-flex align-items-center gap-10">
                  <span class="w-36-px h-36-px bg-base rounded-circle d-flex justify-content-center align-items-center">
                    <img src="@/assets/images/payment/payment-gateway1.png" alt="" />
                  </span>
                  <span class="text-lg fw-semibold text-primary-light">Paypal</span>
                </div>
                <div class="form-switch switch-primary d-flex align-items-center justify-content-center">
                  <input class="form-check-input" type="checkbox" role="switch" v-model="paypalActive" />
                </div>
              </div>
              <div class="card-body p-24">
                <div class="row gy-3">
                  <div class="col-sm-6">
                    <span class="form-label fw-semibold text-primary-light text-md mb-8">Environment <span class="text-danger-600">*</span></span>
                    <div class="d-flex align-items-center gap-3">
                      <div class="d-flex align-items-center gap-10 fw-medium text-lg">
                        <div class="form-check style-check d-flex align-items-center">
                          <input class="form-check-input radius-4 border border-neutral-500" type="checkbox" v-model="paypalSandbox" />
                        </div>
                        <label for="sandbox" class="form-label fw-medium text-lg text-primary-light mb-0">Sandbox</label>
                      </div>
                      <div class="d-flex align-items-center gap-10 fw-medium text-lg">
                        <div class="form-check style-check d-flex align-items-center">
                          <input class="form-check-input radius-4 border border-neutral-500" type="checkbox" v-model="paypalProduction" />
                        </div>
                        <label for="Production" class="form-label fw-medium text-lg text-primary-light mb-0">Production</label>
                      </div>
                    </div>
                  </div>
                  <div class="col-sm-6">
                    <label for="currency" class="form-label fw-semibold text-primary-light text-md mb-8">Currency <span class="text-danger-600">*</span></label>
                    <select class="form-control radius-8 form-select" v-model="paypalCurrency">
                      <option disabled>Select Currency</option>
                      <option>USD</option>
                      <option>TK</option>
                      <option>Rupee</option>
                    </select>
                  </div>
                  <div class="col-sm-6">
                    <label for="secretKey" class="form-label fw-semibold text-primary-light text-md mb-8">Secret Key <span class="text-danger-600">*</span></label>
                    <input type="text" class="form-control radius-8" v-model="paypalSecretKey" placeholder="Secret Key" />
                  </div>
                  <div class="col-sm-6">
                    <label for="publicKey" class="form-label fw-semibold text-primary-light text-md mb-8">Publics Key<span class="text-danger-600">*</span></label>
                    <input type="text" class="form-control radius-8" v-model="paypalPublicKey" placeholder="Publics Key" />
                  </div>
                  <div class="col-sm-6">
                    <label for="logo" class="form-label fw-semibold text-primary-light text-md mb-8">Logo <span class="text-danger-600">*</span></label>
                    <input type="file" class="form-control radius-8" @change="handlePaypalLogoChange" />
                  </div>
                  <div class="col-sm-6">
                    <label class="form-label fw-semibold text-primary-light text-md mb-8"><span class="visibility-hidden">Save</span></label>
                    <button type="submit" class="btn btn-primary border border-primary-600 text-md px-24 py-8 radius-8 w-100 text-center" @click="savePaypal">Save Change</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
  
          <!-- RazorPay Section -->
          <div class="col-xxl-6">
            <div class="card radius-12 shadow-none border overflow-hidden">
              <div class="card-header bg-neutral-100 border-bottom py-16 px-24 d-flex align-items-center flex-wrap gap-3 justify-content-between">
                <div class="d-flex align-items-center gap-10">
                  <span class="w-36-px h-36-px bg-base rounded-circle d-flex justify-content-center align-items-center">
                    <img src="@/assets/images/payment/payment-gateway2.png" alt="" />
                  </span>
                  <span class="text-lg fw-semibold text-primary-light">RazorPay</span>
                </div>
                <div class="form-switch switch-primary d-flex align-items-center justify-content-center">
                  <input class="form-check-input" type="checkbox" role="switch" v-model="razorpayActive" />
                </div>
              </div>
              <div class="card-body p-24">
                <div class="row gy-3">
                  <div class="col-sm-6">
                    <span class="form-label fw-semibold text-primary-light text-md mb-8">Environment <span class="text-danger-600">*</span></span>
                    <div class="d-flex align-items-center gap-3">
                      <div class="d-flex align-items-center gap-10 fw-medium text-lg">
                        <div class="form-check style-check d-flex align-items-center">
                          <input class="form-check-input radius-4 border border-neutral-500" type="checkbox" v-model="razorpaySandbox" />
                        </div>
                        <label for="sandbox2" class="form-label fw-medium text-lg text-primary-light mb-0">Sandbox</label>
                      </div>
                      <div class="d-flex align-items-center gap-10 fw-medium text-lg">
                        <div class="form-check style-check d-flex align-items-center">
                          <input class="form-check-input radius-4 border border-neutral-500" type="checkbox" v-model="razorpayProduction" />
                        </div>
                        <label for="Production2" class="form-label fw-medium text-lg text-primary-light mb-0">Production</label>
                      </div>
                    </div>
                  </div>
                  <div class="col-sm-6">
                    <label for="currencyTwo" class="form-label fw-semibold text-primary-light text-md mb-8">Currency <span class="text-danger-600">*</span></label>
                    <select class="form-control radius-8 form-select" v-model="razorpayCurrency">
                      <option disabled>Select Currency</option>
                      <option>USD</option>
                      <option>TK</option>
                      <option>Rupee</option>
                    </select>
                  </div>
                  <div class="col-sm-6">
                    <label for="secretKeyTwo" class="form-label fw-semibold text-primary-light text-md mb-8">Secret Key <span class="text-danger-600">*</span></label>
                    <input type="text" class="form-control radius-8" v-model="razorpaySecretKey" placeholder="Secret Key" />
                  </div>
                  <div class="col-sm-6">
                    <label for="publicKeyTwo" class="form-label fw-semibold text-primary-light text-md mb-8">Publics Key<span class="text-danger-600">*</span></label>
                    <input type="text" class="form-control radius-8" v-model="razorpayPublicKey" placeholder="Publics Key" />
                  </div>
                  <div class="col-sm-6">
                    <label for="logoTwo" class="form-label fw-semibold text-primary-light text-md mb-8">Logo <span class="text-danger-600">*</span></label>
                    <input type="file" class="form-control radius-8" @change="handleRazorpayLogoChange" />
                  </div>
                  <div class="col-sm-6">
                    <label class="form-label fw-semibold text-primary-light text-md mb-8"><span class="visibility-hidden">Save</span></label>
                    <button type="submit" class="btn btn-primary border border-primary-600 text-md px-24 py-8 radius-8 w-100 text-center" @click="saveRazorpay">Save Change</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
  
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        // Paypal
        paypalActive: true,
        paypalSandbox: true,
        paypalProduction: false,
        paypalCurrency: 'USD',
        paypalSecretKey: 'EGtgNkjt3I5lkhEEzicdot8gVH_PcFiKxx6ZBiXpVrp4QLDYcVQQMLX6MMG_fkS9_H0bwmZzBovb4jLP',
        paypalPublicKey: 'AcRx7vvy79nbNxBemacGKmnnRe_CtxkItyspBS_eeMIPREwfCEIfPg1uX-bdqPrS_ZFGocxEH_SJRrIJ',
        paypalLogo: null,
  
        // RazorPay
        razorpayActive: true,
        razorpaySandbox: true,
        razorpayProduction: false,
        razorpayCurrency: 'USD',
        razorpaySecretKey: 'EGtgNkjt3I5lkhEEzicdot8gVH_PcFiKxx6ZBiXpVrp4QLDYcVQQMLX6MMG_fkS9_H0bwmZzBovb4jLP',
        razorpayPublicKey: 'AcRx7vvy79nbNxBemacGKmnnRe_CtxkItyspBS_eeMIPREwfCEIfPg1uX-bdqPrS_ZFGocxEH_SJRrIJ',
        razorpayLogo: null,
      };
    },
    methods: {
      handlePaypalLogoChange(event) {
        const file = event.target.files[0];
        this.paypalLogo = file;
      },
      handleRazorpayLogoChange(event) {
        const file = event.target.files[0];
        this.razorpayLogo = file;
      },
      savePaypal() {
        console.log("Paypal configuration saved:", this.$data);
      },
      saveRazorpay() {
        console.log("Razorpay configuration saved:", this.$data);
      }
    }
  };
  </script>
  