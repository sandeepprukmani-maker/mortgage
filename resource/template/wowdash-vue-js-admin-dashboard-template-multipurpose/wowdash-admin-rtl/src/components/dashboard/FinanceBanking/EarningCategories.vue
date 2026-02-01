<template>
    <div class="col-md-6">
      <div class="card radius-16 h-100">
        <div class="card-header">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
            <h6 class="mb-2 fw-bold text-lg mb-0">Earning Categories</h6>
            <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
              View All
              <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
            </a>
          </div>
        </div>
        <div class="card-body">
          <div class="d-flex flex-column gap-20">
            <div
              v-for="(category, index) in categories"
              :key="index"
              class="d-flex align-items-center justify-content-between gap-3"
            >
              <div class="d-flex align-items-center w-100 gap-12">
                <span
                  :class="`w-40-px h-40-px rounded-circle d-flex justify-content-center align-items-center ${category.bg}`"
                >
                  <img :src="category.icon" alt="" />
                </span>
                <div class="flex-grow-1">
                  <h6 class="text-sm mb-0">{{ category.title }}</h6>
                  <span class="text-xs text-secondary-light fw-medium">{{ category.subtitle }}</span>
                </div>
              </div>
              <div class="d-flex align-items-center gap-2 w-100">
                <div class="w-100 max-w-66 ms-auto">
                  <div
                    class="progress progress-sm rounded-pill"
                    role="progressbar"
                    aria-label="Success example"
                    :aria-valuenow="category.percent"
                    aria-valuemin="0"
                    aria-valuemax="100"
                  >
                    <div
                      class="progress-bar rounded-pill"
                      :class="category.progressClass"
                      :style="{ width: category.percent + '%' }"
                    ></div>
                  </div>
                </div>
                <span class="text-secondary-light font-xs fw-semibold">{{ category.percent }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import icon1 from '@/assets/images/home-eleven/icons/earn-cat-icon1.svg'
  import icon2 from '@/assets/images/home-eleven/icons/earn-cat-icon2.svg'
  import icon3 from '@/assets/images/home-eleven/icons/earn-cat-icon3.svg'
  import icon4 from '@/assets/images/home-eleven/icons/earn-cat-icon4.svg'

  export default {
    name: 'EarningCategories',
    data() {
      return {
        categories: [
          {
            title: 'Digital Assets',
            subtitle: '$50 / from $1000',
            percent: 80,
            icon: icon1,
            bg: 'bg-primary-100',
            progressClass: 'bg-primary-600',
          },
          {
            title: 'Side Project',
            subtitle: '$50 / from $1000',
            percent: 60,
            icon: icon2,
            bg: 'bg-danger-100',
            progressClass: 'bg-orange',
          },
          {
            title: 'Investment',
            subtitle: '$50 / from $1000',
            percent: 49,
            icon: icon3,
            bg: 'bg-warning-200',
            progressClass: 'bg-yellow',
          },
          {
            title: 'Working Hard',
            subtitle: '$50 / from $1000',
            percent: 100,
            icon: icon4,
            bg: 'bg-success-200',
            progressClass: 'bg-success-main',
          },
        ],
      };
    },
  };
  </script>
  