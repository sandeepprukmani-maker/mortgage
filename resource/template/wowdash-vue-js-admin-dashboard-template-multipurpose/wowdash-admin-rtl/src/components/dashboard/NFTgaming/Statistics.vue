<template>
    <div class="col-xxl-12 col-md-6">
      <div class="card h-100">
        <div class="card-header border-bottom d-flex align-items-center flex-wrap gap-2 justify-content-between">
          <h6 class="fw-bold text-lg mb-0">Statistics</h6>
          <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
            View All
            <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
          </a>
        </div>
        <div class="card-body">
          <div class="d-flex align-items-center gap-1 justify-content-between mb-44">
            <div>
              <h5 class="fw-semibold mb-12">145</h5>
              <span class="text-secondary-light fw-normal text-xl">Total Art Sold</span>
            </div>
            <div id="dailyIconBarChart"></div>
          </div>
          <div class="d-flex align-items-center gap-1 justify-content-between">
            <div>
              <h5 class="fw-semibold mb-12">750 ETH</h5>
              <span class="text-secondary-light fw-normal text-xl">Total Earnings</span>
            </div>
            <div id="areaChart"></div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts';
  import { onMounted } from 'vue';
  
  export default {
    name: 'StatisticsCard',
    setup() {
      const createAreaChart = (chartId, chartColor) => {
        const currentYear = new Date().getFullYear();
        const options = {
          series: [{
            name: 'series1',
            data: [0, 10, 8, 25, 15, 26, 13, 35, 15, 39, 16, 46, 42],
          }],
          chart: {
            type: 'area',
            width: 164,
            height: 72,
            sparkline: { enabled: true },
            toolbar: { show: false },
            padding: { left: 0, right: 0, top: 0, bottom: 0 }
          },
          dataLabels: { enabled: false },
          stroke: {
            curve: 'smooth',
            width: 2,
            colors: [chartColor],
            lineCap: 'round'
          },
          grid: {
            show: true,
            borderColor: 'transparent',
            strokeDashArray: 0,
            position: 'back',
            xaxis: { lines: { show: false } },
            yaxis: { lines: { show: false } },
            row: { colors: undefined, opacity: 0.5 },
            column: { colors: undefined, opacity: 0.5 },
            padding: { top: -3, right: 0, bottom: 0, left: 0 },
          },
          fill: {
            type: 'gradient',
            colors: [chartColor],
            gradient: {
              shade: 'light',
              type: 'vertical',
              shadeIntensity: 0.5,
              gradientToColors: [`${chartColor}00`],
              inverseColors: false,
              opacityFrom: 0.8,
              opacityTo: 0.3,
              stops: [0, 100],
            },
          },
          markers: {
            colors: [chartColor],
            strokeWidth: 2,
            size: 0,
            hover: { size: 8 }
          },
          xaxis: {
            labels: { show: false },
            categories: [
              `Jan ${currentYear}`, `Feb ${currentYear}`, `Mar ${currentYear}`, `Apr ${currentYear}`,
              `May ${currentYear}`, `Jun ${currentYear}`, `Jul ${currentYear}`, `Aug ${currentYear}`,
              `Sep ${currentYear}`, `Oct ${currentYear}`, `Nov ${currentYear}`, `Dec ${currentYear}`
            ],
            tooltip: { enabled: false }
          },
          yaxis: {
            labels: { show: false }
          },
          tooltip: {
            x: { format: 'dd/MM/yy HH:mm' }
          }
        };
  
        const chart = new ApexCharts(document.querySelector(`#${chartId}`), options);
        chart.render();
      };
  
      const createBarChart = () => {
        const options = {
          series: [{
            name: "Sales",
            data: [
              { x: 'Mon', y: 20 },
              { x: 'Tue', y: 40 },
              { x: 'Wed', y: 20 },
              { x: 'Thur', y: 30 },
              { x: 'Fri', y: 40 },
              { x: 'Sat', y: 35 },
            ]
          }],
          chart: {
            type: 'bar',
            width: 164,
            height: 80,
            sparkline: { enabled: true },
            toolbar: { show: false }
          },
          plotOptions: {
            bar: {
              borderRadius: 6,
              horizontal: false,
              columnWidth: 14,
            }
          },
          dataLabels: { enabled: false },
          states: {
            hover: {
              filter: { type: 'none' }
            }
          },
          fill: {
            type: 'gradient',
            colors: ['#E3E6E9'],
            gradient: {
              shade: 'light',
              type: 'vertical',
              shadeIntensity: 0.5,
              gradientToColors: ['#E3E6E9'],
              inverseColors: false,
              opacityFrom: 1,
              opacityTo: 1,
              stops: [0, 100]
            }
          },
          grid: {
            show: false,
            borderColor: '#D1D5DB',
            strokeDashArray: 1,
            position: 'back',
          },
          xaxis: {
            labels: { show: false },
            type: 'category',
            categories: ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat']
          },
          yaxis: {
            labels: {
              show: false,
              formatter: value => (value / 1000).toFixed(0) + 'k'
            }
          },
          tooltip: {
            y: {
              formatter: value => value / 1000 + 'k'
            }
          }
        };
  
        const chart = new ApexCharts(document.querySelector("#dailyIconBarChart"), options);
        chart.render();
      };
  
      onMounted(() => {
        createAreaChart('areaChart', '#FF9F29');
        createBarChart();
      });
    }
  };
  </script>
  