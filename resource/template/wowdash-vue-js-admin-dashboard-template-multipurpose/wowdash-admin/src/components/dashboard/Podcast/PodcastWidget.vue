<template>
    <div class="col-xxl-4 col-lg-5">
      <div class="row gy-4">
        <!-- Total Users Card -->
        <div class="col-lg-12 col-md-6">
          <div class="bg-base radius-12 py-20 px-24 shadow-9">
            <div class="d-flex align-items-center justify-content-between">
              <div>
                <span class="text-secondary-light mb-8">Total Users</span>
                <div class="d-flex align-items-center gap-12">
                  <h6 class="mb-0">17,500</h6>
                  <div class="d-flex align-items-center gap-1 fw-semibold text-success-600">
                    <span>+2.5%</span>
                    <i class="ri-arrow-up-line"></i>
                  </div>
                </div>
              </div>
              <span class="w-60-px h-60-px bg-primary-600 text-white rounded-circle d-flex justify-content-center align-items-center text-2xl primary-shadow">
                <i class="ri-group-fill"></i>
              </span>
            </div>
  
            <div class="mt-32 d-flex align-items-center justify-content-between gap-12 flex-wrap">
              <div class="py-8 px-12 radius-6 gradient-bg-light-one border br-white flex-grow-1">
                <span class="text-secondary-light mb-8 text-sm">Active User:</span>
                <h6 class="mb-0 text-xl">3,500</h6>
              </div>
              <div class="py-8 px-12 radius-6 gradient-bg-light-two border br-white flex-grow-1">
                <span class="text-secondary-light mb-8 text-sm">New Sign ups:</span>
                <h6 class="mb-0 text-xl">5,700</h6>
              </div>
              <div class="py-8 px-12 radius-6 gradient-bg-light-three border br-white flex-grow-1">
                <span class="text-secondary-light mb-8 text-sm">Subscribed:</span>
                <h6 class="mb-0 text-xl">8,000</h6>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Total Podcasts Card -->
        <div class="col-lg-12 col-md-6">
          <div class="bg-base radius-12 py-20 px-24 shadow-9">
            <div class="d-flex align-items-center justify-content-between">
              <div>
                <span class="text-secondary-light mb-8">Total Podcasts</span>
                <div class="d-flex align-items-center gap-12">
                  <h6 class="mb-0">450</h6>
                  <div class="d-flex align-items-center gap-1 fw-semibold text-success-600">
                    <span>+2.5%</span>
                    <i class="ri-arrow-up-line"></i>
                  </div>
                </div>
              </div>
              <span class="w-60-px h-60-px bg-warning-600 text-white rounded-circle d-flex justify-content-center align-items-center text-2xl warning-shadow">
                <i class="ri-mic-fill"></i>
              </span>
            </div>
  
            <div class="mt-32 d-flex align-items-center justify-content-between gap-12 flex-wrap">
              <div class="py-8 px-12 radius-6 gradient-bg-light-four border br-white flex-grow-1">
                <span class="text-secondary-light mb-8 text-sm">Trending:</span>
                <h6 class="mb-0 text-xl">60</h6>
              </div>
              <div class="py-8 px-12 radius-6 gradient-bg-light-five border br-white flex-grow-1">
                <span class="text-secondary-light mb-8 text-sm">Free Podcasts:</span>
                <h6 class="mb-0 text-xl">240</h6>
              </div>
              <div class="py-8 px-12 radius-6 gradient-bg-light-six border br-white flex-grow-1">
                <span class="text-secondary-light mb-8 text-sm">Premium:</span>
                <h6 class="mb-0 text-xl">150</h6>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "PodcastWidget",
  };
  </script>
  