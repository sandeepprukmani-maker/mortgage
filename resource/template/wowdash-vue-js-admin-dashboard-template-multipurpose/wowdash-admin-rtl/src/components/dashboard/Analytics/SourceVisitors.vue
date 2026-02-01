<template>
    <div class="col-xxl-6">
      <div class="card h-100">
        <div class="card-header border-bottom-0 pb-0 d-flex align-items-center flex-wrap gap-2 justify-content-between">
          <h6 class="mb-2 fw-bold text-lg mb-0">Source Visitors</h6>
          <select class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8">
            <option>Last Month</option>
            <option>Last Week</option>
            <option>Last Year</option>
          </select>
        </div>
        <div class="card-body">
          <div class="position-relative h-100 min-h-320-px">
            <div class="md-position-absolute start-0 top-0 mt-20">
              <h6 class="mb-1">524,756</h6>
              <span class="text-secondary-light">Total Platform Visitors</span>
            </div>
            <div class="row g-3 h-100">
              <div
                v-for="(source, index) in sources"
                :key="index"
                class="col-md-3 col-sm-6 d-flex flex-column justify-content-end"
              >
                <div
                  class="d-flex flex-column align-items-center p-24 pt-16 rounded-top-4"
                  :class="source.bgClass"
                  :style="{ minHeight: source.height }"
                >
                  <span
                    class="w-40-px h-40-px d-flex flex-shrink-0 justify-content-center align-items-center rounded-circle mb-12"
                    :class="source.iconBg"
                  >
                    <img :src="source.icon" alt="" />
                  </span>
                  <span class="text-secondary-light">{{ source.name }}</span>
                  <h6 class="mb-0">{{ source.percent }}</h6>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import source1 from '@/assets/images/home-nine/source-icon1.png'
  import source2 from '@/assets/images/home-nine/source-icon2.png'
  import source3 from '@/assets/images/home-nine/source-icon3.png'
  import source4 from '@/assets/images/home-nine/source-icon4.png'

  export default {
    name: 'SourceVisitors',
    data() {
      return {
        sources: [
          {
            name: 'TikTok',
            percent: '50%',
            icon: source1,
            height: '50%',
            bgClass: 'bg-tb-warning',
            iconBg: 'bg-warning-600',
          },
          {
            name: 'Instagram',
            percent: '66%',
            icon: source2,
            height: '66%',
            bgClass: 'bg-tb-lilac',
            iconBg: 'bg-lilac-600',
          },
          {
            name: 'Facebook',
            percent: '82%',
            icon: source3,
            height: '82%',
            bgClass: 'bg-tb-primary',
            iconBg: 'bg-primary-600',
          },
          {
            name: 'Website',
            percent: '96%',
            icon: source4,
            height: '96%',
            bgClass: 'bg-tb-success',
            iconBg: 'bg-success-600',
          },
        ],
      };
    },
  };
  </script>
  
  <style scoped>
  /* No style changes required; all styles inherited via class names */
  </style>
  