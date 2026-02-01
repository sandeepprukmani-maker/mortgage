<template>
    <div class="col-xxl-3 col-lg-6">
      <div class="card h-100 radius-8 border-0">
        <div class="card-body p-24">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
            <h6 class="mb-2 fw-bold text-lg">Customers Statistics</h6>
            <div>
              <select v-model="selectedPeriod" class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8">
                <option>Yearly</option>
                <option>Monthly</option>
                <option>Weekly</option>
                <option>Today</option>
              </select>
            </div>
          </div>
  
          <div class="position-relative">
            <span class="w-80-px h-80-px bg-base shadow text-primary-light fw-semibold text-xl d-flex justify-content-center align-items-center rounded-circle position-absolute end-0 top-0 z-1">+30%</span>
            <div id="statisticsDonutChart" class="mt-36 flex-grow-1 apexcharts-tooltip-z-none title-style circle-none"></div>
            <span class="w-80-px h-80-px bg-base shadow text-primary-light fw-semibold text-xl d-flex justify-content-center align-items-center rounded-circle position-absolute start-0 bottom-0 z-1">+25%</span>
          </div>
          
          <ul class="d-flex flex-wrap align-items-center justify-content-between mt-3 gap-3">
            <li class="d-flex align-items-center gap-2">
              <span class="w-12-px h-12-px radius-2 bg-primary-600"></span>
              <span class="text-secondary-light text-sm fw-normal">Male: 
                <span class="text-primary-light fw-bold">20,000</span>
              </span>
            </li>
            <li class="d-flex align-items-center gap-2">
              <span class="w-12-px h-12-px radius-2 bg-yellow"></span>
              <span class="text-secondary-light text-sm fw-normal">Female:  
                <span class="text-primary-light fw-bold">25,000</span>
              </span>
            </li>
          </ul>
  
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts'
  import VueApexCharts from 'vue3-apexcharts'
  
  export default {
    name: 'CustomerStatistics',
    components: {
      apexchart: VueApexCharts
    },
    data() {
      return {
        selectedPeriod: 'Yearly', // Default value for the select
        chartOptions: {
          series: [30, 25],
          colors: ['#FF9F29', '#487FFF'],
          labels: ['Female', 'Male'],
          legend: {
            show: false 
          },
          chart: {
            type: 'donut',
            height: 230,
            sparkline: {
              enabled: true // Remove whitespace
            },
            margin: {
              top: 0,
              right: 0,
              bottom: 0,
              left: 0
            },
            padding: {
              top: 0,
              right: 0,
              bottom: 0,
              left: 0
            }
          },
          stroke: {
            width: 0,
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
          }],
        }
      }
    },
    mounted() {
      this.renderChart();
    },
    methods: {
      renderChart() {
        const chart = new ApexCharts(document.querySelector("#statisticsDonutChart"), this.chartOptions);
        chart.render();
      }
    }
  }
  </script>
  
  <style scoped>
  /* Add any additional styles here if needed */
  </style>
  