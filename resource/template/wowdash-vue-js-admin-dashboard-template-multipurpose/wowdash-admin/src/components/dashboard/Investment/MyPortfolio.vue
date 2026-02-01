<template>
    <div class="col-xxl-3">
      <div class="card h-100 radius-8 border-0">
        <div class="card-body p-24">
          <h6 class="mb-2 fw-bold text-lg">My Portfolio</h6>
  
          <div class="position-relative">
            <span class="w-80-px h-80-px bg-base shadow text-primary-light fw-bold text-xxl d-flex justify-content-center align-items-center rounded-circle position-absolute end-0 top-0 z-1">20k</span>
            
            <!-- Use the apexchart component directly -->
            <apexchart
              id="statisticsDonutChart"
              class="mt-36 flex-grow-1 apexcharts-tooltip-z-none title-style circle-none"
              :options="chartOptions"
              :series="chartSeries"
              type="donut"
              height="230"
            ></apexchart>
  
            <span class="w-80-px h-80-px bg-base shadow text-primary-light fw-bold text-xxl d-flex justify-content-center align-items-center rounded-circle position-absolute start-0 bottom-0 z-1">50k</span>
          </div>
  
          <ul class="d-flex flex-wrap flex-column mt-64 gap-3">
            <li class="d-flex align-items-center gap-2">
              <span class="w-16-px h-16-px radius-2 bg-primary-600"></span>
              <span class="text-secondary-light text-lg fw-normal">Total Gain:
                <span class="text-primary-light fw-bold text-lg">$50,000</span>
              </span>
            </li>
            <li class="d-flex align-items-center gap-2">
              <span class="w-16-px h-16-px radius-2 bg-yellow"></span>
              <span class="text-secondary-light text-lg fw-normal">Total Investment:
                <span class="text-primary-light fw-bold text-lg">$20,000</span>
              </span>
            </li>
          </ul>
  
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import VueApexCharts from 'vue3-apexcharts'
  
  export default {
    name: 'MyPortfolio',
    components: {
      apexchart: VueApexCharts
    },
    data() {
      return {
        chartSeries: [70, 30],
        chartOptions: {
          labels: ['Female', 'Male'],
          colors: ['#FF9F29', '#487FFF'],
          legend: {
            show: false
          },
          chart: {
            type: 'donut',
            sparkline: {
              enabled: true
            }
          },
          stroke: {
            width: 0
          },
          dataLabels: {
            enabled: false
          },
          responsive: [{
            breakpoint: 480,
            options: {
              chart: {
                width: 200
              },
              legend: {
                position: 'bottom'
              }
            }
          }]
        }
      }
    }
  }
  </script>
  