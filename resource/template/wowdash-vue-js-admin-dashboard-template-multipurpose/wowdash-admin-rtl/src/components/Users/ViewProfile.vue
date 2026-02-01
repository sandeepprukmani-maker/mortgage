<template>
    <div class="row gy-4">
      <div class="col-lg-4">
        <div class="user-grid-card position-relative border radius-16 overflow-hidden bg-base h-100">
          <img src="@/assets/images/user-grid/user-grid-bg1.png" alt="" class="w-100 object-fit-cover" />
          <div class="pb-24 ms-16 mb-24 me-16 mt--100">
            <div class="text-center border border-top-0 border-start-0 border-end-0">
              <!-- <img
                :src="profileImage || '@/assets/images/user-grid/user-grid-img14.png'"
                alt=""
                class="border br-white border-width-2-px w-200-px h-200-px rounded-circle object-fit-cover"
              /> -->
              <img src='@/assets/images/user-grid/user-grid-img14.png' alt=""
                class="border br-white border-width-2-px w-200-px h-200-px rounded-circle object-fit-cover"
              />
              <h6 class="mb-0 mt-16">Jacob Jones</h6>
              <span class="text-secondary-light mb-16">ifrandom@gmail.com</span>
            </div>
            <div class="mt-24">
              <h6 class="text-xl mb-16">Personal Info</h6>
              <ul>
                <li class="d-flex align-items-center gap-1 mb-12">
                  <span class="w-30 text-md fw-semibold text-primary-light">Full Name</span>
                  <span class="w-70 text-secondary-light fw-medium">: Will Jonto</span>
                </li>
                <li class="d-flex align-items-center gap-1 mb-12">
                  <span class="w-30 text-md fw-semibold text-primary-light"> Email</span>
                  <span class="w-70 text-secondary-light fw-medium">: willjontoax@gmail.com</span>
                </li>
                <li class="d-flex align-items-center gap-1 mb-12">
                  <span class="w-30 text-md fw-semibold text-primary-light"> Phone Number</span>
                  <span class="w-70 text-secondary-light fw-medium">: (1) 2536 2561 2365</span>
                </li>
                <li class="d-flex align-items-center gap-1 mb-12">
                  <span class="w-30 text-md fw-semibold text-primary-light"> Department</span>
                  <span class="w-70 text-secondary-light fw-medium">: Design</span>
                </li>
                <li class="d-flex align-items-center gap-1 mb-12">
                  <span class="w-30 text-md fw-semibold text-primary-light"> Designation</span>
                  <span class="w-70 text-secondary-light fw-medium">: UI UX Designer</span>
                </li>
                <li class="d-flex align-items-center gap-1 mb-12">
                  <span class="w-30 text-md fw-semibold text-primary-light"> Languages</span>
                  <span class="w-70 text-secondary-light fw-medium">: English</span>
                </li>
                <li class="d-flex align-items-center gap-1">
                  <span class="w-30 text-md fw-semibold text-primary-light"> Bio</span>
                  <span class="w-70 text-secondary-light fw-medium">: Lorem Ipsum is simply dummy text of the printing and typesetting industry.</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Right Panel -->
      <div class="col-lg-8">
        <div class="card h-100">
          <div class="card-body p-24">
            <!-- Tabs -->
            <ul class="nav border-gradient-tab nav-pills mb-20 d-inline-flex" role="tablist">
              <li class="nav-item" role="presentation">
                <button class="nav-link d-flex align-items-center px-24" :class="{ active: activeTab === 'edit-profile' }" @click="activeTab = 'edit-profile'">
                  Edit Profile
                </button>
              </li>
              <li class="nav-item" role="presentation">
                <button class="nav-link d-flex align-items-center px-24" :class="{ active: activeTab === 'change-password' }" @click="activeTab = 'change-password'">
                  Change Password
                </button>
              </li>
              <li class="nav-item" role="presentation">
                <button class="nav-link d-flex align-items-center px-24" :class="{ active: activeTab === 'notification' }" @click="activeTab = 'notification'">
                  Notification Settings
                </button>
              </li>
            </ul>
  
            <!-- Tabs Content -->
            <div class="tab-content">
              <!-- Edit Profile Tab -->
              <div v-if="activeTab === 'edit-profile'">
                <h6 class="text-md text-primary-light mb-16">Profile Image</h6>
                <div class="mb-24 mt-16">
                  <div class="avatar-upload">
                    <div class="avatar-edit position-absolute bottom-0 end-0 me-24 mt-16 z-1 cursor-pointer">
                      <input type="file" id="imageUpload" accept=".png, .jpg, .jpeg" @change="onImageChange" hidden />
                      <label for="imageUpload" class="w-32-px h-32-px d-flex justify-content-center align-items-center bg-primary-50 text-primary-600 border border-primary-600 bg-hover-primary-100 text-lg rounded-circle">
                        <iconify-icon icon="solar:camera-outline" class="icon"></iconify-icon>
                      </label>
                    </div>
                    <div class="avatar-preview">
                      <div id="imagePreview" :style="{ backgroundImage: 'url(' + profileImage + ')' }"></div>
                    </div>
                  </div>
                </div>
  
                <!-- Profile Form -->
                <form action="#">
                  <div class="row">
                    <!-- Full Name -->
                    <div class="col-sm-6 mb-20">
                      <label class="form-label fw-semibold text-primary-light text-sm mb-8">Full Name <span class="text-danger-600">*</span></label>
                      <input type="text" class="form-control radius-8" placeholder="Enter Full Name" />
                    </div>
                    <!-- Email -->
                    <div class="col-sm-6 mb-20">
                      <label class="form-label fw-semibold text-primary-light text-sm mb-8">Email <span class="text-danger-600">*</span></label>
                      <input type="email" class="form-control radius-8" placeholder="Enter email address" />
                    </div>
                    <!-- Phone -->
                    <div class="col-sm-6 mb-20">
                      <label class="form-label fw-semibold text-primary-light text-sm mb-8">Phone</label>
                      <input type="text" class="form-control radius-8" placeholder="Enter phone number" />
                    </div>
                    <!-- Department -->
                    <div class="col-sm-6 mb-20">
                      <label class="form-label fw-semibold text-primary-light text-sm mb-8">Department <span class="text-danger-600">*</span></label>
                      <select class="form-control radius-8 form-select">
                        <option>Enter Event Title</option>
                        <option>Enter Event Title One</option>
                        <option>Enter Event Title Two</option>
                      </select>
                    </div>
                    <!-- Designation -->
                    <div class="col-sm-6 mb-20">
                      <label class="form-label fw-semibold text-primary-light text-sm mb-8">Designation <span class="text-danger-600">*</span></label>
                      <select class="form-control radius-8 form-select">
                        <option>Enter Designation Title</option>
                        <option>Enter Designation Title One</option>
                        <option>Enter Designation Title Two</option>
                      </select>
                    </div>
                    <!-- Language -->
                    <div class="col-sm-6 mb-20">
                      <label class="form-label fw-semibold text-primary-light text-sm mb-8">Language <span class="text-danger-600">*</span></label>
                      <select class="form-control radius-8 form-select">
                        <option>English</option>
                        <option>Bangla</option>
                        <option>Hindi</option>
                        <option>Arabic</option>
                      </select>
                    </div>
                    <!-- Description -->
                    <div class="col-sm-12 mb-20">
                      <label class="form-label fw-semibold text-primary-light text-sm mb-8">Description</label>
                      <textarea class="form-control radius-8" placeholder="Write description..."></textarea>
                    </div>
                  </div>
  
                  <div class="d-flex align-items-center justify-content-center gap-3">
                    <button type="button" class="border border-danger-600 bg-hover-danger-200 text-danger-600 text-md px-56 py-11 radius-8">Cancel</button>
                    <button type="button" class="btn btn-primary border border-primary-600 text-md px-56 py-12 radius-8">Save</button>
                  </div>
                </form>
              </div>
  
              <!-- Change Password Tab -->
              <div v-if="activeTab === 'change-password'">
                <div class="mb-20">
                  <label class="form-label fw-semibold text-primary-light text-sm mb-8">New Password <span class="text-danger-600">*</span></label>
                  <div class="position-relative">
                    <input :type="passwordVisible ? 'text' : 'password'" class="form-control radius-8" placeholder="Enter New Password*" />
                    <span @click="togglePassword" class="ri-eye-line cursor-pointer position-absolute end-0 top-50 translate-middle-y me-16 text-secondary-light"></span>
                  </div>
                </div>
                <div class="mb-20">
                  <label class="form-label fw-semibold text-primary-light text-sm mb-8">Confirmed Password <span class="text-danger-600">*</span></label>
                  <div class="position-relative">
                    <input :type="passwordVisible ? 'text' : 'password'" class="form-control radius-8" placeholder="Confirm Password*" />
                    <span @click="togglePassword" class="ri-eye-line cursor-pointer position-absolute end-0 top-50 translate-middle-y me-16 text-secondary-light"></span>
                  </div>
                </div>
              </div>
  
              <!-- Notification Settings Tab -->
              <div v-if="activeTab === 'notification'">
                <div v-for="(label, key) in notifications" :key="key" class="form-switch switch-primary py-12 px-16 border radius-8 position-relative mb-16">
                  <label :for="key" class="position-absolute w-100 h-100 start-0 top-0"></label>
                  <div class="d-flex align-items-center gap-3 justify-content-between">
                    <span class="form-check-label line-height-1 fw-medium text-secondary-light">{{ label.name }}</span>
                    <input class="form-check-input" type="checkbox" role="switch" :id="key" v-model="label.enabled" />
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
  import user1 from "@/assets/images/user-grid/user-grid-img13.png";

  export default {
    data() {
      return {
        activeTab: 'edit-profile',
        profileImage: user1,
        passwordVisible: false,
        notifications: {
          companzNew: { name: 'Company News', enabled: false },
          pushNotifcation: { name: 'Push Notification', enabled: true },
          weeklyLetters: { name: 'Weekly News Letters', enabled: true },
          meetUp: { name: 'Meetups Near you', enabled: false },
          orderNotification: { name: 'Orders Notifications', enabled: true },
        },
      };
    },
    methods: {
      onImageChange(event) {
        const file = event.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = e => {
            this.profileImage = e.target.result;
          };
          reader.readAsDataURL(file);
        }
      },
      togglePassword() {
        this.passwordVisible = !this.passwordVisible;
      },
    },
  };
  </script>
  