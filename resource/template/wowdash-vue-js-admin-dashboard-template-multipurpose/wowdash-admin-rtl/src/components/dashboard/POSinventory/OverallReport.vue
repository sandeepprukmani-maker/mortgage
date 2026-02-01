<template>
    <div class="col-xxl-4 col-md-6">
      <div class="card h-100">
        <div class="card-header">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
            <h6 class="mb-2 fw-bold text-lg">Overall Report</h6>
            <select v-model="selectedTimeframe" class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8">
              <option>Yearly</option>
              <option>Monthly</option>
              <option>Weekly</option>
              <option>Today</option>
            </select>
          </div>
        </div>
        <div class="card-body p-24">
          <div class="mt-32">
            <div id="userOverviewDonutChart" class="mx-auto apexcharts-tooltip-z-none"></div>
          </div>
          <div class="d-flex flex-wrap gap-20 justify-content-center mt-48">
            <div class="d-flex align-items-center gap-8">
              <span class="w-16-px h-16-px radius-2 bg-primary-600"></span>
              <span class="text-secondary-light">Purchase</span>
            </div>
            <div class="d-flex align-items-center gap-8">
              <span class="w-16-px h-16-px radius-2 bg-lilac-600"></span>
              <span class="text-secondary-light">Sales</span>
            </div>
            <div class="d-flex align-items-center gap-8">
              <span class="w-16-px h-16-px radius-2 bg-warning-600"></span>
              <span class="text-secondary-light">Expense</span>
            </div>
            <div class="d-flex align-items-center gap-8">
              <span class="w-16-px h-16-px radius-2 bg-success-600"></span>
              <span class="text-secondary-light">Gross Profit</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts';
  import VueApexCharts from 'vue3-apexcharts';
  
  export default {
    components: {
      apexchart: VueApexCharts,
    },
    data() {
      return {
        selectedTimeframe: 'Yearly', // Default selection for the dropdown
        options: {
          series: [30, 30, 20, 20],
          colors: ['#FF9F29', '#487FFF', '#45B369', '#9935FE'],
          labels: ['Purchase', 'Sales', 'Expense', 'Gross Profit'],
          legend: {
            show: false
          },
          chart: {
            type: 'donut',
            height: 270,
            sparkline: {
              enabled: true
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
            enabled: true
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
        },
      };
    },
    mounted() {
      this.renderChart();
    },
    watch: {
      selectedTimeframe(newVal) {
        this.renderChart(); // Re-render chart when timeframe selection changes
      }
    },
    methods: {
      renderChart() {
        const chart = new ApexCharts(document.querySelector("#userOverviewDonutChart"), this.options);
        chart.render();
      }
    }
  };
  </script>