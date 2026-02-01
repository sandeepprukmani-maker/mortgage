<template>
      <!-- Doctors Card -->
      <div class="col-xxl-3 col-xl-4 col-sm-6">
        <div class="card p-3 shadow-2 radius-8 h-100 bg-gradient-end-6">
          <div class="card-body p-0">
            <div class="d-flex flex-wrap align-items-center justify-content-between gap-1 mb-8">
              <div class="d-flex align-items-center gap-2">
                <span class="mb-0 w-48-px h-48-px bg-cyan-100 text-cyan-600 flex-shrink-0 text-white d-flex justify-content-center align-items-center rounded-circle h6 mb-0">
                  <i class="ri-group-fill"></i>
                </span>
                <div>
                  <h6 class="fw-semibold mb-2">650</h6>
                  <span class="fw-medium text-secondary-light text-sm">Doctors</span>
                </div>
              </div>
            </div>
            <p class="text-sm mb-0">
              <span class="text-cyan-600">4</span> Doctors joined this week
            </p>
          </div>
        </div>
      </div>
  
      <!-- Staffs Card -->
      <div class="col-xxl-3 col-xl-4 col-sm-6">
        <div class="card p-3 shadow-2 radius-8 h-100 bg-gradient-end-4">
          <div class="card-body p-0">
            <div class="d-flex flex-wrap align-items-center justify-content-between gap-1 mb-8">
              <div class="d-flex align-items-center gap-2">
                <span class="mb-0 w-48-px h-48-px bg-lilac-100 text-lilac-600 flex-shrink-0 text-white d-flex justify-content-center align-items-center rounded-circle h6 mb-0">
                  <i class="ri-award-fill"></i>
                </span>
                <div>
                  <h6 class="fw-semibold mb-2">570</h6>
                  <span class="fw-medium text-secondary-light text-sm">Staffs</span>
                </div>
              </div>
            </div>
            <p class="text-sm mb-0">
              <span class="text-lilac-600">8</span> Staffs on vacation
            </p>
          </div>
        </div>
      </div>
  
      <!-- Patients Card -->
      <div class="col-xxl-3 col-xl-4 col-sm-6">
        <div class="card p-3 shadow-2 radius-8 h-100 bg-gradient-end-1">
          <div class="card-body p-0">
            <div class="d-flex flex-wrap align-items-center justify-content-between gap-1 mb-8">
              <div class="d-flex align-items-center gap-2">
                <span class="mb-0 w-48-px h-48-px bg-primary-100 text-primary-600 flex-shrink-0 text-white d-flex justify-content-center align-items-center rounded-circle h6 mb-0">
                  <i class="ri-group-fill"></i>
                </span>
                <div>
                  <h6 class="fw-semibold mb-2">15,750</h6>
                  <span class="fw-medium text-secondary-light text-sm">Patients</span>
                </div>
              </div>
            </div>
            <p class="text-sm mb-0">
              <span class="text-primary-600">170</span> New patients admitted
            </p>
          </div>
        </div>
      </div>
  
      <!-- Pharmacies Card -->
      <div class="col-xxl-3 col-xl-4 col-sm-6">
        <div class="card p-3 shadow-2 radius-8 h-100 bg-gradient-end-1">
          <div class="card-body p-0">
            <div class="d-flex flex-wrap align-items-center justify-content-between gap-1 mb-8">
              <div class="d-flex align-items-center gap-2">
                <span class="mb-0 w-48-px h-48-px bg-success-100 text-success-600 flex-shrink-0 text-white d-flex justify-content-center align-items-center rounded-circle h6 mb-0">
                  <i class="ri-wallet-3-fill"></i>
                </span>
                <div>
                  <h6 class="fw-semibold mb-2">$42,400</h6>
                  <span class="fw-medium text-secondary-light text-sm">Pharmacies</span>
                </div>
              </div>
            </div>
            <p class="text-sm mb-0">
              <span class="text-success-600">60,000</span> Medicine on reserve
            </p>
          </div>
        </div>
      </div>
  </template>
  
  <script>
  export default {
    name: 'DashboardCards',
  };
  </script>
  