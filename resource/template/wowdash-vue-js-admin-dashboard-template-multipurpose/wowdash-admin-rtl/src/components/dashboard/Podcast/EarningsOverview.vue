<template>
    <div class="col-lg-4">
      <div class="bg-base radius-12 py-20 px-24 shadow-9 h-100 mb-20">
        <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
          <h6 class="mb-0 fw-bold text-lg">Earnings Overview</h6>
          <select class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8">
            <option>Yearly</option>
            <option>Monthly</option>
            <option>Weekly</option>
            <option>Today</option>
          </select>
        </div>
        <ul class="d-flex flex-wrap align-items-center justify-content-center mt-24 gap-3">
          <li class="d-flex align-items-center gap-2">
            <span class="w-8-px h-8-px rounded-circle bg-primary-600"></span>
            <span class="text-secondary-light text-sm fw-medium d-inline-flex align-items-center gap-1">
              Income:
              <span class="text-primary-light text-xl fw-bold">$26,201</span>
            </span>
            <div class="d-flex align-items-center gap-1 fw-semibold text-success-600">
              <span>10%</span>
              <i class="ri-arrow-up-s-fill"></i>
            </div>
          </li>
        </ul>
        <div class="mt-24">
          <div id="revenueChart" ref="chartContainer" class="apexcharts-tooltip-style-1"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts';
  
  export default {
    name: 'EarningsOverview',
    mounted() {
      this.createChart('revenueChart', '#98B6FF', '#6593FF');
    },
    methods: {
      createChart(chartId, color1, color2) {
        const options = {
          series: [
            {
              name: 'series1',
              data: [6, 20, 15, 48, 28, 55, 28, 52, 25, 32, 15, 25],
            },
          ],
          legend: {
            show: false,
          },
          chart: {
            type: 'area',
            width: '100%',
            height: 200,
            toolbar: { show: false },
            padding: { left: 0, right: 0, top: 0, bottom: 0 },
          },
          dataLabels: { enabled: false },
          stroke: {
            curve: 'smooth',
            width: 0,
            colors: [color1, color2],
            lineCap: 'round',
          },
          grid: {
            show: true,
            borderColor: '#D1D5DB',
            strokeDashArray: 1,
            position: 'back',
            xaxis: { lines: { show: false } },
            yaxis: { lines: { show: true } },
            row: { colors: undefined, opacity: 0.5 },
            column: { colors: undefined, opacity: 0.5 },
            padding: { top: -20, right: 0, bottom: -10, left: 0 },
          },
          colors: [color1, color2],
          fill: {
            type: 'gradient',
            colors: [color1, color2],
            gradient: {
              shade: 'light',
              type: 'vertical',
              shadeIntensity: 0.5,
              gradientToColors: [undefined, `${color2}00`],
              inverseColors: false,
              opacityFrom: [1, 0.6],
              opacityTo: [0.5, 0.4],
              stops: [0, 100],
            },
          },
          markers: {
            colors: [color1, color2],
            strokeWidth: 2,
            size: 0,
            hover: { size: 8 },
          },
          xaxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            tooltip: { enabled: false },
            labels: {
              formatter: value => value,
              style: { fontSize: '14px' },
            },
          },
          yaxis: {
            tickAmount:6,
            labels: {
              formatter: value => `$${value}k`,
              style: { fontSize: '14px' },
            },
          },
          tooltip: {
            x: { format: 'dd/MM/yy HH:mm' },
          },
        };
  
        const chart = new ApexCharts(this.$refs.chartContainer, options);
        chart.render();
      },
    },
  };
  </script>
  