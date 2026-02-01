<template>
    <div class="col-xxl-6">
      <div class="card h-100">
        <div class="card-body">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
            <h6 class="mb-2 fw-bold text-lg mb-0">Generated Content</h6>
            <select v-model="timePeriod" class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8">
              <option>Today</option>
              <option>Weekly</option>
              <option>Monthly</option>
              <option>Yearly</option>
            </select>
          </div>
  
          <ul class="d-flex flex-wrap align-items-center mt-3 gap-3">
            <li class="d-flex align-items-center gap-2">
              <span class="w-12-px h-12-px rounded-circle bg-primary-600"></span>
              <span class="text-secondary-light text-sm fw-semibold">Word:
                <span class="text-primary-light fw-bold">500</span>
              </span>
            </li>
            <li class="d-flex align-items-center gap-2">
              <span class="w-12-px h-12-px rounded-circle bg-yellow"></span>
              <span class="text-secondary-light text-sm fw-semibold">Image:
                <span class="text-primary-light fw-bold">300</span>
              </span>
            </li>
          </ul>
  
          <div class="mt-40">
            <div id="paymentStatusChart" class="margin-16-minus"></div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts';
  import VueApexCharts from 'vue3-apexcharts';
  
  export default {
    name: 'GeneratedContent',
    components: {
      apexchart: VueApexCharts
    },
    data() {
      return {
        timePeriod: 'Today', // Default selected time period
        chartOptions: {
          series: [
            {
              name: 'Net Profit',
              data: [20000, 16000, 14000, 25000, 45000, 18000, 28000, 11000, 26000, 48000, 18000, 22000]
            },
            {
              name: 'Revenue',
              data: [15000, 18000, 19000, 20000, 35000, 20000, 18000, 13000, 18000, 38000, 14000, 16000]
            }
          ],
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
            }
          },
          grid: {
            show: true,
            borderColor: '#D1D5DB',
            strokeDashArray: 4, // Use a number for dashed style
            position: 'back'
          },
          plotOptions: {
            bar: {
              borderRadius: 4,
              columnWidth: 10
            }
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
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
          },
          yaxis: {
            categories: ['0', '5000', '10,000', '20,000', '30,000', '50,000', '60,000', '60,000', '70,000', '80,000', '90,000', '100,000']
          },
          fill: {
            opacity: 1,
            width: 18
          }
        }
      };
    },
    mounted() {
      // Initialize the chart after the component has been mounted
      this.renderChart();
    },
    methods: {
      renderChart() {
        const chart = new ApexCharts(document.querySelector("#paymentStatusChart"), this.chartOptions);
        chart.render();
      }
    }
  };
  </script>