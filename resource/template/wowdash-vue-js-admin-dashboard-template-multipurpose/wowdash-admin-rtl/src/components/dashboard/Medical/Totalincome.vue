<template>
    <div class="col-xxl-12 col-xl-6">
      <div class="card h-100 radius-8 border-0">
        <div class="card-header border-bottom d-flex align-items-center flex-wrap gap-2 justify-content-between">
          <h6 class="mb-2 fw-bold text-lg">Total Income</h6>
          <div>
            <select class="form-select form-select-sm w-auto bg-base border-0 text-secondary-light">
              <option>This Month</option>
              <option>This Week</option>
              <option>This Year</option>
            </select>
          </div>
        </div>
        <div class="card-body p-24">
          <div class="position-relative">
            <apexchart
              id="statisticsDonutChart"
              class="mt-36 flex-grow-1 apexcharts-tooltip-z-none title-style circle-none"
              type="donut"
              :options="chartOptions"
              :series="series"
              height="260"
            ></apexchart>
            <div class="text-center position-absolute top-50 start-50 translate-middle">
              <span class="text-secondary-light">Income</span>
              <h6>$28,500</h6>
            </div>
          </div>
  
          <ul class="row gy-4 mt-3">
            <li class="col-6 d-flex flex-column align-items-center">
              <div class="d-flex align-items-center gap-2">
                <span class="w-12-px h-8-px rounded-pill bg-warning-600"></span>
                <span class="text-secondary-light text-sm fw-normal">Net Income</span>
              </div>
              <h6 class="text-primary-light fw-bold mb-0">$50,000</h6>
            </li>
            <li class="col-6 d-flex flex-column align-items-center">
              <div class="d-flex align-items-center gap-2">
                <span class="w-12-px h-8-px rounded-pill bg-success-600"></span>
                <span class="text-secondary-light text-sm fw-normal">Commission</span>
              </div>
              <h6 class="text-primary-light fw-bold mb-0">$20,000</h6>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexChart from 'vue3-apexcharts';
  
  export default {
    name: 'TotalIncomeCard',
    components: {
      apexchart: ApexChart
    },
    data() {
      return {
        series: [30, 25],
        chartOptions: {
          chart: {
            type: 'donut',
            height: 260,
            sparkline: { enabled: true },
            margin: { top: 0, right: 0, bottom: 0, left: 0 },
            padding: { top: 0, right: 0, bottom: 0, left: 0 }
          },
          colors: ['#FF9F29', '#45B369'],
          labels: ['Female', 'Male'],
          legend: {
            show: false
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
      };
    }
  };
  </script>
  