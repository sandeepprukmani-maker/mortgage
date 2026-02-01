<template>
    <div class="col-xxl-4 col-md-6">
      <div class="card h-100">
        <div class="card-header">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
            <h6 class="mb-2 fw-bold text-lg mb-0">Purchase & Sales</h6>
            <select v-model="selectedTimeframe" class="form-select form-select-sm w-auto bg-base text-secondary-light">
              <option>This Month</option>
              <option>This Week</option>
              <option>This Year</option>
            </select>
          </div>
        </div>
        <div class="card-body p-24">
          <ul class="d-flex flex-wrap align-items-center justify-content-center my-3 gap-3">
            <li class="d-flex align-items-center gap-2">
              <span class="w-12-px h-8-px rounded-pill bg-warning-600"></span>
              <span class="text-secondary-light text-sm fw-semibold">Purchase: $<span class="text-primary-light fw-bold">500</span></span>
            </li>
            <li class="d-flex align-items-center gap-2">
              <span class="w-12-px h-8-px rounded-pill bg-success-600"></span>
              <span class="text-secondary-light text-sm fw-semibold">Sales: $<span class="text-primary-light fw-bold">800</span></span>
            </li>
          </ul>
          <div id="purchaseSaleChart" class="margin-16-minus y-value-left"></div>
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
        selectedTimeframe: 'This Month', // Default selection for the dropdown
        options: {
          series: [
            {
              name: 'Net Profit',
              data: [44, 100, 40, 56, 30, 58, 50],
            },
            {
              name: 'Free Cash',
              data: [60, 120, 60, 90, 50, 95, 90],
            },
          ],
          colors: ['#45B369', '#FF9F29'],
          labels: ['Active', 'New', 'Total'],
          legend: {
            show: false,
          },
          chart: {
            type: 'bar',
            height: 260,
            toolbar: {
              show: false,
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
              columnWidth: 8,
            },
          },
          dataLabels: {
            enabled: false,
          },
          states: {
            hover: {
              filter: {
                type: 'none',
              },
            },
          },
          stroke: {
            show: true,
            width: 0,
            colors: ['transparent'],
          },
          yaxis: {
            min:0,
            max:120,
            tickAmount: 4,
          },
          xaxis: {
            categories: ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun'],
          },
          fill: {
            opacity: 1,
            width: 18,
          },
        },
      };
    },
    mounted() {
      this.renderChart();
    },
    watch: {
      selectedTimeframe(newVal) {
        this.renderChart(); // Re-render chart when timeframe selection changes
      },
    },
    methods: {
      renderChart() {
        const chart = new ApexCharts(document.querySelector("#purchaseSaleChart"), this.options);
        chart.render();
      },
    },
  };
  </script>