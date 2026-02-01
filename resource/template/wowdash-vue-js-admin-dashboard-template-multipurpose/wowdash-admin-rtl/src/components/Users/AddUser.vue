<template>
    <div class="card h-100 p-0 radius-12">
      <div class="card-body p-24">
        <div class="row justify-content-center">
          <div class="col-xxl-6 col-xl-8 col-lg-10">
            <div class="card border">
              <div class="card-body">
                <h6 class="text-md text-primary-light mb-16">Profile Image</h6>
  
                <!-- Upload Image Start -->
                <div class="mb-24 mt-16">
                  <div class="avatar-upload">
                    <div class="avatar-edit position-absolute bottom-0 end-0 me-24 mt-16 z-1 cursor-pointer">
                      <input
                        type="file"
                        id="imageUpload"
                        accept=".png, .jpg, .jpeg"
                        @change="onImageChange"
                        hidden
                      />
                      <label
                        for="imageUpload"
                        class="w-32-px h-32-px d-flex justify-content-center align-items-center bg-primary-50 text-primary-600 border border-primary-600 bg-hover-primary-100 text-lg rounded-circle"
                      >
                        <iconify-icon icon="solar:camera-outline" class="icon"></iconify-icon>
                      </label>
                    </div>
                    <div class="avatar-preview">
                      <div
                        v-bind:style="{ backgroundImage: 'url(' + imagePreview + ')' }"
                        id="imagePreview"
                      ></div>
                    </div>
                  </div>
                </div>
                <!-- Upload Image End -->
  
                <form @submit.prevent="submitForm">
                  <div class="mb-20">
                    <label for="name" class="form-label fw-semibold text-primary-light text-sm mb-8">
                      Full Name <span class="text-danger-600">*</span>
                    </label>
                    <input
                      v-model="form.name"
                      type="text"
                      class="form-control radius-8"
                      id="name"
                      placeholder="Enter Full Name"
                    />
                  </div>
                  <div class="mb-20">
                    <label for="email" class="form-label fw-semibold text-primary-light text-sm mb-8">
                      Email <span class="text-danger-600">*</span>
                    </label>
                    <input
                      v-model="form.email"
                      type="email"
                      class="form-control radius-8"
                      id="email"
                      placeholder="Enter email address"
                    />
                  </div>
                  <div class="mb-20">
                    <label for="number" class="form-label fw-semibold text-primary-light text-sm mb-8">
                      Phone
                    </label>
                    <input
                      v-model="form.phone"
                      type="text"
                      class="form-control radius-8"
                      id="number"
                      placeholder="Enter phone number"
                    />
                  </div>
                  <div class="mb-20">
                    <label for="depart" class="form-label fw-semibold text-primary-light text-sm mb-8">
                      Department <span class="text-danger-600">*</span>
                    </label>
                    <select v-model="form.department" class="form-control radius-8 form-select" id="depart">
                      <option value="">Enter Event Title</option>
                      <option>Enter Event Title One</option>
                      <option>Enter Event Title Two</option>
                    </select>
                  </div>
                  <div class="mb-20">
                    <label for="desig" class="form-label fw-semibold text-primary-light text-sm mb-8">
                      Designation <span class="text-danger-600">*</span>
                    </label>
                    <select v-model="form.designation" class="form-control radius-8 form-select" id="desig">
                      <option value="">Enter Designation Title</option>
                      <option>Enter Designation Title One</option>
                      <option>Enter Designation Title Two</option>
                    </select>
                  </div>
                  <div class="mb-20">
                    <label for="desc" class="form-label fw-semibold text-primary-light text-sm mb-8">
                      Description
                    </label>
                    <textarea
                      v-model="form.description"
                      class="form-control radius-8"
                      id="desc"
                      placeholder="Write description..."
                    ></textarea>
                  </div>
                  <div class="d-flex align-items-center justify-content-center gap-3">
                    <button
                      type="button"
                      class="border border-danger-600 bg-hover-danger-200 text-danger-600 text-md px-56 py-11 radius-8"
                      @click="cancelForm"
                    >
                      Cancel
                    </button>
                    <button
                      type="submit"
                      class="btn btn-primary border border-primary-600 text-md px-56 py-12 radius-8"
                    >
                      Save
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import user1 from "@/assets/images/user-grid/user-grid-img13.png";
  export default {
    data() {
      return {
        form: {
          name: '',
          email: '',
          phone: '',
          department: '',
          designation: '',
          description: '',
        },
        imagePreview: user1,
      };
    },
    methods: {
      onImageChange(event) {
        const file = event.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = (e) => {
            console.log("image,",e.target.result)
            this.imagePreview = e.target.result;
          };
          reader.readAsDataURL(file);
        }
      },
      cancelForm() {
        this.form = {
          name: '',
          email: '',
          phone: '',
          department: '',
          designation: '',
          description: '',
        };
        this.imagePreview = user1;
      },
      submitForm() {
        // Handle form submission
        console.log(this.form);
        // You can make an API call here to save the data
      },
    },
  };
  </script>
  