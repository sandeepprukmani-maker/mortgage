<template>
  <div class="col-xxl-4 col-md-6">
      <div class="card radius-8 border-0 d-flex flex-column" style="height: 530px;">

          <div class="card-body d-flex flex-column h-100">
              <!-- Header -->
              <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between mb-3">
                  <h6 class="fw-bold text-lg">Countries Status</h6>
                  <select class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8">
                      <option>Yearly</option>
                      <option>Today</option>
                      <option>Weekly</option>
                      <option>Monthly</option>
                  </select>
              </div>

              <!-- Map -->
              <div ref="mapContainer" class="world-map mb-3"></div>

              <!-- Scrollable Country List -->
              <div class="scrollable-country-list">
                  <div class="d-flex align-items-center justify-content-between gap-3 mb-3 pb-2"
                      v-for="(country, index) in countries" :key="index">
                      <div class="d-flex align-items-center w-100">
                          <img :src="country.flag" :alt="country.name + ' flag'"
                              class="w-40-px h-40-px rounded-circle flex-shrink-0 me-12 overflow-hidden" />
                          <div class="flex-grow-1">
                              <h6 class="text-sm mb-0">{{ country.name }}</h6>
                              <span class="text-xs text-secondary-light fw-medium">{{ country.users }} Users</span>
                          </div>
                      </div>
                      <div class="d-flex align-items-center gap-2 w-100">
                          <div class="w-100 max-w-66 ms-auto">
                              <div class="progress progress-sm rounded-pill" role="progressbar"
                                  :aria-valuenow="country.progress" aria-valuemin="0" aria-valuemax="100">
                                  <div class="progress-bar" :class="country.progressColor"
                                      :style="{ width: country.progress + '%' }">
                                  </div>
                              </div>
                          </div>
                          <span class="text-secondary-light font-xs fw-semibold">{{ country.progress }}%</span>
                      </div>
                  </div>
              </div>
          </div>
      </div>
  </div>
</template>



<script>
import { onMounted, ref } from 'vue';
import jsVectorMap from 'jsvectormap';
import 'jsvectormap/dist/maps/world.js';

import flag1 from '@/assets/images/flags/flag1.png'
import flag2 from '@/assets/images/flags/flag2.png'
import flag3 from '@/assets/images/flags/flag3.png'
import flag4 from '@/assets/images/flags/flag4.png'
import flag5 from '@/assets/images/flags/flag5.png'

export default {
  name: 'WorldMap',
  setup() {
      const mapContainer = ref(null);
      // console.log(mapContainer);

      // Country data for the progress bars
      const countries = ref([
          { name: 'USA', flag: flag1, users: '1,240', progress: 80, progressColor: 'bg-primary-600' },
          { name: 'Japan', flag: flag2, users: '1,240', progress: 60, progressColor: 'bg-orange' },
          { name: 'France', flag: flag3, users: '1,240', progress: 49, progressColor: 'bg-yellow' },
          { name: 'Germany', flag: flag4, users: '1,240', progress: 100, progressColor: 'bg-success-main' },
          { name: 'South Korea', flag: flag5, users: '1,240', progress: 30, progressColor: 'bg-info-main' },
          { name: 'USA', flag: flag1, users: '1,240', progress: 80, progressColor: 'bg-primary-600' },
      ]);
      console.log(countries);

      onMounted(() => {
          if (mapContainer.value) {
              // console.log(mapContainer);

              // Initialize map
              new jsVectorMap({
                  selector: mapContainer.value,
                  map: 'world',
                  backgroundColor: 'transparent',
                  regionStyle: {
                      initial: {
                          fill: '#D1D5DB',
                      },
                      hover: {
                          fill: '#A5B4FC',
                      },
                      selected: {
                          fill: '#3B82F6',
                      },
                  },
                  markers: [
                      { coords: [35.8617, 104.1954], name: 'China: 250' },
                      { coords: [25.2744, 133.7751], name: 'Australia: 250' },
                      { coords: [36.77, -119.41], name: 'USA: 82%' },
                      { coords: [55.37, -3.41], name: 'UK: 250' },
                      { coords: [25.20, 55.27], name: 'UAE: 250' },
                  ],
                  markerStyle: {
                      initial: {
                          fill: '#ffffff',
                          stroke: '#000',
                          'stroke-width': 1,
                          r: 6,
                      },
                      hover: {
                          fill: '#e9edf7',
                      },
                  },
                  series: {
                      regions: [
                          {
                              values: {
                                  US: 1,
                                  CN: 1,
                                  AU: 1,
                                  GB: 1,
                                  AE: 1,
                              },
                              scale: ['#D1D5DB', '#487FFF'], // from gray to blue
                              normalizeFunction: 'polynomial',
                              attribute: 'fill',
                          },
                      ],
                  },
                  zoomButtons: true,
                  zoomOnScroll: false,
              });
          }
      });

      return { mapContainer, countries };
  },
};
</script>

<style>
/* Add styles to ensure correct height behavior */
.card-body {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  min-height: 0;
}

.row {
  display: flex;
}

.col-lg-6 {
  flex: 1;
}

h6 {
  font-size: 16px;
  font-weight: bold;
}

.text-sm {
  font-size: 14px;
}

.text-xs {
  font-size: 12px;
}

.progress-bar {
  transition: width 0.4s ease-in-out;
}

.jvm-zoom-btn.jvm-zoomin,
.jvm-zoom-btn.jvm-zoomout {
  position: absolute !important;
  display: flex;
  justify-content: center;
  align-items: center;
}

.jvm-zoom-btn.jvm-zoomin {
  top: 10px !important;
  left: 10px !important;
}

.jvm-zoom-btn.jvm-zoomout {
  top: 30px !important;
  left: 10px !important;
}

.jvm-zoomin,
.jvm-zoomout {
  width: 15px;
  height: 15px;
  background-color: #D1D5DB;
  border: 1px solid #ccc;
  color: #111827;
  font-size: 18px;
  line-height: 28px;
  text-align: center;
  border-radius: 4px;
  cursor: pointer;
}

.world-map {
  height: 300px;
  /* or any height you want for the map */
  border-radius: 8px;
  position: relative;
}

.scrollable-country-list {
  overflow-y: auto;
  flex-grow: 1;
  max-height: 300px;
  /* adjust as needed */
  padding-right: 4px;
}

.w-40-px {
  width: 40px;
}

.h-40-px {
  height: 40px;
}

.max-w-66 {
  max-width: 66px;
}

.text-sm {
  font-size: 14px;
}

.text-xs {
  font-size: 12px;
}

.text-lg {
  font-size: 1.125rem;
}

.font-xs {
  font-size: 0.75rem;
}

.progress-bar {
  transition: width 0.4s ease-in-out;
}
</style>