<template>
    <div class="card h-100 p-0 radius-12 overflow-hidden">
      <div class="card-body p-40">
        <form @submit.prevent="handleSubmit">
          <div class="row">
            <div class="col-sm-6">
              <div class="mb-20">
                <label for="name" class="form-label fw-semibold text-primary-light text-sm mb-8">
                  Full Name <span class="text-danger-600">*</span>
                </label>
                <input
                  v-model="formData.name"
                  type="text"
                  class="form-control radius-8"
                  id="name"
                  placeholder="Enter Full Name"
                  required
                />
              </div>
            </div>
            <div class="col-sm-6">
              <div class="mb-20">
                <label for="email" class="form-label fw-semibold text-primary-light text-sm mb-8">
                  Email <span class="text-danger-600">*</span>
                </label>
                <input
                  v-model="formData.email"
                  type="email"
                  class="form-control radius-8"
                  id="email"
                  placeholder="Enter email address"
                  required
                />
              </div>
            </div>
            <div class="col-sm-6">
              <div class="mb-20">
                <label for="number" class="form-label fw-semibold text-primary-light text-sm mb-8">
                  Phone Number
                </label>
                <input
                  v-model="formData.phone"
                  type="text"
                  class="form-control radius-8"
                  id="number"
                  placeholder="Enter phone number"
                />
              </div>
            </div>
            <div class="col-sm-6">
              <div class="mb-20">
                <label for="website" class="form-label fw-semibold text-primary-light text-sm mb-8">
                  Website
                </label>
                <input
                  v-model="formData.website"
                  type="url"
                  class="form-control radius-8"
                  id="website"
                  placeholder="Website URL"
                />
              </div>
            </div>
            <div class="col-sm-6">
              <div class="mb-20">
                <label for="country" class="form-label fw-semibold text-primary-light text-sm mb-8">
                  Country <span class="text-danger-600">*</span>
                </label>
                <select
                  v-model="formData.country"
                  class="form-control radius-8 form-select"
                  id="country"
                  required
                >
                  <option value="" disabled selected>Select Country</option>
                  <option>USA</option>
                  <option>Bangladesh</option>
                  <option>Pakistan</option>
                  <option>India</option>
                  <option>Canada</option>
                </select>
              </div>
            </div>
            <div class="col-sm-6">
              <div class="mb-20">
                <label for="city" class="form-label fw-semibold text-primary-light text-sm mb-8">
                  City <span class="text-danger-600">*</span>
                </label>
                <select
                  v-model="formData.city"
                  class="form-control radius-8 form-select"
                  id="city"
                  required
                >
                  <option value="" disabled selected>Select City</option>
                  <option>Washington</option>
                  <option>Dhaka</option>
                  <option>Lahore</option>
                  <option>Punjab</option>
                </select>
              </div>
            </div>
            <div class="col-sm-6">
              <div class="mb-20">
                <label for="state" class="form-label fw-semibold text-primary-light text-sm mb-8">
                  State <span class="text-danger-600">*</span>
                </label>
                <select
                  v-model="formData.state"
                  class="form-control radius-8 form-select"
                  id="state"
                  required
                >
                  <option value="" disabled selected>Select State</option>
                  <option>Washington</option>
                  <option>Dhaka</option>
                  <option>Lahore</option>
                  <option>Punjab</option>
                </select>
              </div>
            </div>
            <div class="col-sm-6">
              <div class="mb-20">
                <label for="zip" class="form-label fw-semibold text-primary-light text-sm mb-8">
                  Zip Code <span class="text-danger-600">*</span>
                </label>
                <input
                  v-model="formData.zip"
                  type="text"
                  class="form-control radius-8"
                  id="zip"
                  placeholder="Zip Code"
                  required
                />
              </div>
            </div>
            <div class="col-sm-12">
              <div class="mb-20">
                <label for="address" class="form-label fw-semibold text-primary-light text-sm mb-8">
                  Address* <span class="text-danger-600">*</span>
                </label>
                <input
                  v-model="formData.address"
                  type="text"
                  class="form-control radius-8"
                  id="address"
                  placeholder="Enter Your Address"
                  required
                />
              </div>
            </div>
            <div class="d-flex align-items-center justify-content-center gap-3 mt-24">
              <button
                type="reset"
                class="border border-danger-600 bg-hover-danger-200 text-danger-600 text-md px-40 py-11 radius-8"
                @click="resetForm"
              >
                Reset
              </button>
              <button type="submit" class="btn btn-primary border border-primary-600 text-md px-24 py-12 radius-8">
                Save Change
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        formData: {
          name: "",
          email: "",
          phone: "",
          website: "",
          country: "",
          city: "",
          state: "",
          zip: "",
          address: "",
        },
      };
    },
    methods: {
      handleSubmit() {
        // Handle form submission logic here
        console.log("Form Submitted", this.formData);
      },
      resetForm() {
        this.formData = {
          name: "",
          email: "",
          phone: "",
          website: "",
          country: "",
          city: "",
          state: "",
          zip: "",
          address: "",
        };
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add your custom styles here if needed */
  </style>
  