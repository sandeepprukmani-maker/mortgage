<template>
    <div class="col-xxl-12 col-sm-6">
      <div class="card h-100 radius-8 border-0">
        <div class="card-body p-24">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
            <h6 class="mb-2 fw-bold text-lg">Campaigns</h6>
            <div>
              <select v-model="selectedPeriod" class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8">
                <option value="Yearly">Yearly</option>
                <option value="Monthly">Monthly</option>
                <option value="Weekly">Weekly</option>
                <option value="Today">Today</option>
              </select>
            </div>
          </div>
          
          <div class="mt-3">
            
            <div v-for="(campaign, index) in campaigns" :key="index" class="d-flex align-items-center justify-content-between gap-3 mb-12">
              <div class="d-flex align-items-center">
                <span :class="`text-xxl line-height-1 d-flex align-content-center flex-shrink-0 ${campaign.iconClass}`">
                  <iconify-icon :icon="campaign.icon" class="icon"></iconify-icon>
                </span>
                <span class="text-primary-light fw-medium text-sm ps-12">{{ campaign.name }}</span>
              </div>
              <div class="d-flex align-items-center gap-2 w-100">
                <div class="w-100 max-w-66 ms-auto">
                  <div class="progress progress-sm rounded-pill" role="progressbar" :aria-valuenow="campaign.progress" aria-valuemin="0" aria-valuemax="100">
                    <div class="progress-bar" :class="`bg-${campaign.progressBarColor} rounded-pill`" :style="{ width: `${campaign.progress}%` }"></div>
                  </div>
                </div>
                <span class="text-secondary-light font-xs fw-semibold">{{ campaign.progress }}%</span>
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
        selectedPeriod: 'Yearly', // Default selected period
        campaigns: [
          {
            name: 'Email',
            icon: 'majesticons:mail',
            iconClass: 'text-orange',
            progress: 80,
            progressBarColor: 'orange',
          },
          {
            name: 'Website',
            icon: 'eva:globe-2-fill',
            iconClass: 'text-success-main',
            progress: 60,
            progressBarColor: 'success-main',
          },
          {
            name: 'Facebook',
            icon: 'fa6-brands:square-facebook',
            iconClass: 'text-info-main',
            progress: 49,
            progressBarColor: 'info-main',
          },
          {
            name: 'Email',
            icon: 'fluent:location-off-20-filled',
            iconClass: 'text-indigo',
            progress: 70,
            progressBarColor: 'indigo',
          },
        ],
      };
    },
  };
  </script>
  
  <style scoped>
  .icon {
    font-size: 24px;
  }
  </style>
  