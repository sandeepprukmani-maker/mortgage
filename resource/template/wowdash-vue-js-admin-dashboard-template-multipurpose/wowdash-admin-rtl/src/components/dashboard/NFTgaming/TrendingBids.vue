<template>
    <div class="col-12">
      <h6 class="mb-16">Trending Bids</h6>
      <div class="row gy-4">
        <!-- Dashboard Widget Start -->
        <div class="col-lg-4 col-sm-6">
          <div class="card px-24 py-16 shadow-none radius-12 border h-100 bg-gradient-start-3">
            <div class="card-body p-0">
              <div class="d-flex flex-wrap align-items-center justify-content-between gap-1">
                <div class="d-flex align-items-center flex-wrap gap-16">
                  <span class="mb-0 w-40-px h-40-px bg-primary-600 flex-shrink-0 text-white d-flex justify-content-center align-items-center rounded-circle h6 mb-0">
                    <iconify-icon icon="flowbite:users-group-solid" class="icon"></iconify-icon>
                  </span>
                  <div class="flex-grow-1">
                    <h6 class="fw-semibold mb-0">24,000</h6>
                    <span class="fw-medium text-secondary-light text-md">Artworks</span>
                    <p class="text-sm mb-0 d-flex align-items-center flex-wrap gap-12 mt-12">
                      <span class="bg-success-focus px-6 py-2 rounded-2 fw-medium text-success-main text-sm d-flex align-items-center gap-8">
                        +168.001%
                        <i class="ri-arrow-up-line"></i>
                      </span>
                      This week
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- Dashboard Widget End -->
  
        <!-- Dashboard Widget Start -->
        <div class="col-lg-4 col-sm-6">
          <div class="card px-24 py-16 shadow-none radius-12 border h-100 bg-gradient-start-5">
            <div class="card-body p-0">
              <div class="d-flex flex-wrap align-items-center justify-content-between gap-1">
                <div class="d-flex align-items-center flex-wrap gap-16">
                  <span class="mb-0 w-40-px h-40-px bg-primary-600 flex-shrink-0 text-white d-flex justify-content-center align-items-center rounded-circle h6 mb-0">
                    <iconify-icon icon="flowbite:users-group-solid" class="icon"></iconify-icon>
                  </span>
                  <div class="flex-grow-1">
                    <h6 class="fw-semibold mb-0">82,000</h6>
                    <span class="fw-medium text-secondary-light text-md">Auction</span>
                    <p class="text-sm mb-0 d-flex align-items-center flex-wrap gap-12 mt-12">
                      <span class="bg-danger-focus px-6 py-2 rounded-2 fw-medium text-danger-main text-sm d-flex align-items-center gap-8">
                        +168.001%
                        <i class="ri-arrow-down-line"></i>
                      </span>
                      This week
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- Dashboard Widget End -->
  
        <!-- Dashboard Widget Start -->
        <div class="col-lg-4 col-sm-6">
          <div class="card px-24 py-16 shadow-none radius-12 border h-100 bg-gradient-start-2">
            <div class="card-body p-0">
              <div class="d-flex flex-wrap align-items-center justify-content-between gap-1">
                <div class="d-flex align-items-center flex-wrap gap-16">
                  <span class="mb-0 w-40-px h-40-px bg-primary-600 flex-shrink-0 text-white d-flex justify-content-center align-items-center rounded-circle h6 mb-0">
                    <iconify-icon icon="flowbite:users-group-solid" class="icon"></iconify-icon>
                  </span>
                  <div class="flex-grow-1">
                    <h6 class="fw-semibold mb-0">800</h6>
                    <span class="fw-medium text-secondary-light text-md">Creators</span>
                    <p class="text-sm mb-0 d-flex align-items-center flex-wrap gap-12 mt-12">
                      <span class="bg-success-focus px-6 py-2 rounded-2 fw-medium text-success-main text-sm d-flex align-items-center gap-8">
                        +168.001%
                        <i class="ri-arrow-up-line"></i>
                      </span>
                      This week
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- Dashboard Widget End -->
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "TrendingBids",
  };
  </script>