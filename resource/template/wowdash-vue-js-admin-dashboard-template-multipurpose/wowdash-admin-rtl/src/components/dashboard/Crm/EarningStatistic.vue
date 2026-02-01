<template>
    <div class="col-xxl-8">
      <div class="card h-100 radius-8 border-0">
        <div class="card-body p-24">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
            <div>
              <h6 class="mb-2 fw-bold text-lg">Earning Statistic</h6>
              <span class="text-sm fw-medium text-secondary-light">Yearly earning overview</span>
            </div>
            <div>
              <select v-model="selectedPeriod" class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8">
                <option value="yearly">Yearly</option>
                <option value="monthly">Monthly</option>
                <option value="weekly">Weekly</option>
                <option value="today">Today</option>
              </select>
            </div>
          </div>
  
          <div class="mt-20 d-flex justify-content-center flex-wrap gap-3">
            <div
              v-for="(stat, index) in statistics"
              :key="index"
              class="d-inline-flex align-items-center gap-2 p-2 radius-8 border pe-36 br-hover-primary group-item"
            >
              <span class="bg-neutral-100 w-44-px h-44-px text-xxl radius-8 d-flex justify-content-center align-items-center text-secondary-light group-hover:bg-primary-600 group-hover:text-white">
                <iconify-icon :icon="stat.icon" class="icon"></iconify-icon>
              </span>
              <div>
                <span class="text-secondary-light text-sm fw-medium">{{ stat.title }}</span>
                <h6 class="text-md fw-semibold mb-0">{{ stat.amount }}</h6>
              </div>
            </div>
          </div>
  
          <div id="barChart" class="barChart mt-4"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { onMounted, ref } from 'vue';
  import ApexCharts from 'apexcharts';
  
  export default {
    name: 'EarningStatistic',
    setup() {
      const selectedPeriod = ref('yearly');
  
      const statistics = ref([
        { title: 'Sales', amount: '$200k', icon: 'fluent:cart-16-filled' },
        { title: 'Income', amount: '$200k', icon: 'uis:chart' },
        { title: 'Profit', amount: '$200k', icon: 'ph:arrow-fat-up-fill' },
      ]);
  
      const initChart = () => {
        const options = {
          series: [{
            name: "Sales",
            data: [
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
              { x: 'Dec', y: 50000 },
            ],
          }],
          chart: {
            type: 'bar',
            height: 310,
            toolbar: {
              show: false,
            },
          },
          plotOptions: {
            bar: {
              borderRadius: 4,
              horizontal: false,
              columnWidth: '23%',
              endingShape: 'rounded',
            },
          },
          dataLabels: {
            enabled: false,
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
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
          },
          yaxis: {
            labels: {
              formatter: function (value) {
                return (value / 1000).toFixed(0) + 'k';
              },
            },
          },
          tooltip: {
            y: {
              formatter: function (value) {
                return (value / 1000) + 'k';
              },
            },
          },
        };
  
        const chart = new ApexCharts(document.querySelector("#barChart"), options);
        chart.render();
      };
  
      onMounted(() => {
        initChart();
      });
  
      return {
        selectedPeriod,
        statistics,
      };
    },
  };
  </script>
  
  <style scoped>
  /* You can move the styles here if you need scoped customizations */
  </style>
  