<template>
    <div class="col-xxl-9">
      <div class="card radius-8 border-0">
        <div class="row">
          <div class="col-xxl-6 pe-xxl-0">
            <div class="card-body p-24">
              <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
                <h6 class="mb-2 fw-bold text-lg">Revenue Report</h6>
                <div>
                  <select v-model="selectedPeriod" class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8">
                    <option>Yearly</option>
                    <option>Monthly</option>
                    <option>Weekly</option>
                    <option>Today</option>
                  </select>
                </div>
              </div>
              <ul class="d-flex flex-wrap align-items-center mt-3 gap-3">
                <li class="d-flex align-items-center gap-2">
                  <span class="w-12-px h-12-px radius-2 bg-primary-600"></span>
                  <span class="text-secondary-light text-sm fw-semibold">Earning: 
                    <span class="text-primary-light fw-bold">$500,00,000.00</span>
                  </span>
                </li>
                <li class="d-flex align-items-center gap-2">
                  <span class="w-12-px h-12-px radius-2 bg-yellow"></span>
                  <span class="text-secondary-light text-sm fw-semibold">Expense: 
                    <span class="text-primary-light fw-bold">$20,000.00</span>
                  </span>
                </li>
              </ul>
              <div class="mt-40">
                <div id="paymentStatusChart" class="margin-16-minus"></div>
              </div>
            </div>
          </div>
          <div class="col-xxl-6">
            <div class="row h-100 g-0">
              <div class="col-6 p-0 m-0">
                <div class="card-body p-24 h-100 d-flex flex-column justify-content-center border border-top-0">
                  <div class="d-flex flex-wrap align-items-center justify-content-between gap-1 mb-8">
                    <div>
                      <span class="mb-12 w-44-px h-44-px text-primary-600 bg-primary-light border border-primary-light-white flex-shrink-0 d-flex justify-content-center align-items-center radius-8 h6 mb-12">
                        <iconify-icon icon="fa-solid:box-open" class="icon"></iconify-icon>  
                      </span>
                      <span class="mb-1 fw-medium text-secondary-light text-md">Total Products</span>
                      <h6 class="fw-semibold text-primary-light mb-1">300</h6>
                    </div>
                  </div>
                  <p class="text-sm mb-0">Increase by  <span class="bg-success-focus px-1 rounded-2 fw-medium text-success-main text-sm">+200</span> this week</p>
                </div>
              </div>
              <div class="col-6 p-0 m-0">
                <div class="card-body p-24 h-100 d-flex flex-column justify-content-center border border-top-0 border-start-0 border-end-0">
                  <div class="d-flex flex-wrap align-items-center justify-content-between gap-1 mb-8">
                    <div>
                      <span class="mb-12 w-44-px h-44-px text-yellow bg-yellow-light border border-yellow-light-white flex-shrink-0 d-flex justify-content-center align-items-center radius-8 h6 mb-12">
                        <iconify-icon icon="flowbite:users-group-solid" class="icon"></iconify-icon>  
                      </span>
                      <span class="mb-1 fw-medium text-secondary-light text-md">Total Customer</span>
                      <h6 class="fw-semibold text-primary-light mb-1">50,000</h6>
                    </div>
                  </div>
                  <p class="text-sm mb-0">Increase by  <span class="bg-danger-focus px-1 rounded-2 fw-medium text-danger-main text-sm">-5k</span> this week</p>
                </div>
              </div>
              <div class="col-6 p-0 m-0">
                <div class="card-body p-24 h-100 d-flex flex-column justify-content-center border border-top-0 border-bottom-0">
                  <div class="d-flex flex-wrap align-items-center justify-content-between gap-1 mb-8">
                    <div>
                      <span class="mb-12 w-44-px h-44-px text-lilac bg-lilac-light border border-lilac-light-white flex-shrink-0 d-flex justify-content-center align-items-center radius-8 h6 mb-12">
                        <iconify-icon icon="majesticons:shopping-cart" class="icon"></iconify-icon>  
                      </span>
                      <span class="mb-1 fw-medium text-secondary-light text-md">Total Orders</span>
                      <h6 class="fw-semibold text-primary-light mb-1">1500</h6>
                    </div>
                  </div>
                  <p class="text-sm mb-0">Increase by  <span class="bg-success-focus px-1 rounded-2 fw-medium text-success-main text-sm">+1k</span> this week</p>
                </div>
              </div>
              <div class="col-6 p-0 m-0">
                <div class="card-body p-24 h-100 d-flex flex-column justify-content-center border border-top-0 border-start-0 border-end-0 border-bottom-0">
                  <div class="d-flex flex-wrap align-items-center justify-content-between gap-1 mb-8">
                    <div>
                      <span class="mb-12 w-44-px h-44-px text-pink bg-pink-light border border-pink-light-white flex-shrink-0 d-flex justify-content-center align-items-center radius-8 h6 mb-12">
                        <iconify-icon icon="ri:discount-percent-fill" class="icon"></iconify-icon>  
                      </span>
                      <span class="mb-1 fw-medium text-secondary-light text-md">Total Sales</span>
                      <h6 class="fw-semibold text-primary-light mb-1">$25,00,000.00</h6>
                    </div>
                  </div>
                  <p class="text-sm mb-0">Increase by  <span class="bg-success-focus px-1 rounded-2 fw-medium text-success-main text-sm">+$10k</span> this week</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts'
  import VueApexCharts from 'vue3-apexcharts'
  
  export default {
    name: 'RevenueReport',
    components: {
      apexchart: VueApexCharts
    },
    data() {
      return {
        selectedPeriod: 'Yearly', // Default value for the select
        chartOptions: {
          series: [{
            name: 'Net Profit',
            data: [20000, 16000, 14000, 25000, 45000, 18000, 28000, 11000, 26000, 48000, 18000, 22000]
          }, {
            name: 'Revenue',
            data: [15000, 18000, 19000, 20000, 35000, 20000, 18000, 13000, 18000, 38000, 14000, 16000]
          }],
          colors: ['#487FFF', '#FF9F29'],
          labels: ['Active', 'New', 'Total'],
          legend: {
            show: false 
          },
          chart: {
            type: 'bar',
            height: 250,
            toolbar: {
              show: false
            },
          },
          grid: {
            show: true,
            borderColor: '#D1D5DB',
            strokeDashArray: 4,
            position: 'back',
          },
          plotOptions: {
            bar: {
              borderRadius: 4,
              columnWidth: 10,
            },
          },
          dataLabels: {
            enabled: false
          },
          stroke: {
            show: true,
            width: 2,
            colors: ['transparent']
          },
          xaxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
          },
          yaxis: {
            categories: ['0', '5000', '10,000', '20,000', '30,000', '50,000', '60,000', '60,000', '70,000', '80,000', '90,000', '100,000'],
          },
          fill: {
            opacity: 1,
            width: 18,
          },
        }
      }
    },
    mounted() {
      this.renderChart();
    },
    methods: {
      renderChart() {
        const chart = new ApexCharts(document.querySelector("#paymentStatusChart"), this.chartOptions);
        chart.render();
      }
    }
  }
  </script>