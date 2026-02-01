<template>
    <div class="col-xxl-8 col-lg-6">
      <div class="card h-100 border shadow-none radius-8 border-0">
        <div class="card-body p-24">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
            <div>
              <h6 class="mb-2 fw-bold text-lg">Earning Statistic</h6>
              <span class="text-sm fw-medium text-secondary-light">Yearly earning overview</span>
            </div>
            <div>
              <select class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8" v-model="selectedPeriod">
                <option>Yearly</option>
                <option>Monthly</option>
                <option>Weekly</option>
                <option>Today</option>
              </select>
            </div>
          </div>
  
          <div class="mt-20 d-flex justify-content-center flex-wrap gap-3">
            <div class="d-inline-flex align-items-center gap-2 p-2 radius-8 border pe-36 br-hover-primary group-item">
              <span class="bg-neutral-100 w-44-px h-44-px text-xxl radius-8 d-flex justify-content-center align-items-center text-secondary-light group-hover:bg-primary-600 group-hover:text-white">
                <iconify-icon icon="fluent:cart-16-filled" class="icon"></iconify-icon>
              </span>
              <div>
                <span class="text-secondary-light text-sm fw-medium">Sales</span>
                <h6 class="text-md fw-semibold mb-0">$200k</h6>
              </div>
            </div>
  
            <div class="d-inline-flex align-items-center gap-2 p-2 radius-8 border pe-36 br-hover-primary group-item">
              <span class="bg-neutral-100 w-44-px h-44-px text-xxl radius-8 d-flex justify-content-center align-items-center text-secondary-light group-hover:bg-primary-600 group-hover:text-white">
                <iconify-icon icon="uis:chart" class="icon"></iconify-icon>
              </span>
              <div>
                <span class="text-secondary-light text-sm fw-medium">Income</span>
                <h6 class="text-md fw-semibold mb-0">$200k</h6>
              </div>
            </div>
  
            <div class="d-inline-flex align-items-center gap-2 p-2 radius-8 border pe-36 br-hover-primary group-item">
              <span class="bg-neutral-100 w-44-px h-44-px text-xxl radius-8 d-flex justify-content-center align-items-center text-secondary-light group-hover:bg-primary-600 group-hover:text-white">
                <iconify-icon icon="ph:arrow-fat-up-fill" class="icon"></iconify-icon>
              </span>
              <div>
                <span class="text-secondary-light text-sm fw-medium">Profit</span>
                <h6 class="text-md fw-semibold mb-0">$200k</h6>
              </div>
            </div>
          </div>
  
          <div id="barChart" class="barChart"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts';
  import { ref, onMounted } from 'vue';
  
  export default {
    name: 'EarningStatistic',
    setup() {
      const selectedPeriod = ref('Yearly');
  
      const chartData = [
        { x: 'Jan', y: 85000 },
        { x: 'Feb', y: 70000 },
        { x: 'Mar', y: 40000 },
        { x: 'Apr', y: 50000 },
        { x: 'May', y: 60000 },
        { x: 'Jun', y: 50000 },
        { x: 'Jul', y: 40000 },
        { x: 'Aug', y: 50000 },
        { x: 'Sep', y: 40000 },
        { x: 'Oct', y: 60000 },
        { x: 'Nov', y: 30000 },
        { x: 'Dec', y: 50000 }
      ];
  
      onMounted(() => {
        const options = {
          series: [{
            name: 'Sales',
            data: chartData
          }],
          chart: {
            type: 'bar',
            height: 310,
            toolbar: {
              show: false
            }
          },
          plotOptions: {
            bar: {
              borderRadius: 4,
              horizontal: false,
              columnWidth: '23%',
              endingShape: 'rounded',
            }
          },
          dataLabels: {
            enabled: false
          },
          fill: {
            type: 'gradient',
            colors: ['#487FFF'],
            gradient: {
              shade: 'light',
              type: 'vertical',
              shadeIntensity: 0.5,
              gradientToColors: ['#487FFF'],
              inverseColors: false,
              opacityFrom: 1,
              opacityTo: 1,
              stops: [0, 100],
            },
          },
          grid: {
            show: true,
            borderColor: '#D1D5DB',
            strokeDashArray: 4,
            position: 'back',
          },
          xaxis: {
            type: 'category',
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
          },
          yaxis: {
            labels: {
              formatter: function (value) {
                return (value / 1000).toFixed(0) + 'k';
              }
            }
          },
          tooltip: {
            y: {
              formatter: function (value) {
                return value / 1000 + 'k';
              }
            }
          }
        };
  
        const chart = new ApexCharts(document.querySelector("#barChart"), options);
        chart.render();
      });
  
      return { selectedPeriod };
    }
  };
  </script>