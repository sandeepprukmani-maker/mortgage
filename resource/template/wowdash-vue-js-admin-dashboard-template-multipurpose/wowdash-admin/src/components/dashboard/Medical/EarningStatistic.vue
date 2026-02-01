<template>
    <div class="col-xxl-12">
      <div class="card h-100">
        <div class="card-header">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
            <h6 class="mb-2 fw-bold text-lg mb-0">Earning Statistic</h6>
            <select class="form-select form-select-sm w-auto bg-base border-0 text-secondary-light">
              <option>This Month</option>
              <option>This Week</option>
              <option>This Year</option>
            </select>
          </div>
        </div>
        <div class="card-body p-24">
          <ul class="d-flex flex-wrap align-items-center justify-content-center my-3 gap-3">
            <li class="d-flex align-items-center gap-2">
              <span class="w-12-px h-8-px rounded-pill bg-primary-600"></span>
              <span class="text-secondary-light text-sm fw-semibold">
                New Patient:
                <span class="text-primary-light fw-bold">50</span>
              </span>
            </li>
            <li class="d-flex align-items-center gap-2">
              <span class="w-12-px h-8-px rounded-pill bg-warning-600"></span>
              <span class="text-secondary-light text-sm fw-semibold">
                Old Patient:
                <span class="text-primary-light fw-bold">500</span>
              </span>
            </li>
          </ul>
          <div id="enrollmentChart" class="apexcharts-tooltip-style-1"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts';
  
  export default {
    name: 'EarningStatisticCard',
    mounted() {
      this.createChartTwo('enrollmentChart', '#487FFF', '#FF9F29');
    },
    methods: {
      createChartTwo(chartId, color1, color2) {
        const options = {
          series: [
            {
              name: 'New Patient',
              data: [48, 35, 55, 32, 48, 30, 55, 50, 57],
            },
            {
              name: 'Old Patient',
              data: [12, 20, 15, 26, 22, 60, 40, 48, 25],
            },
          ],
          legend: { show: false },
          chart: {
            type: 'area',
            width: '100%',
            height: 270,
            toolbar: { show: false },
            padding: { left: 0, right: 0, top: 0, bottom: 0 },
          },
          dataLabels: { enabled: false },
          stroke: {
            curve: 'smooth',
            width: 3,
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
              opacityFrom: [0.4, 0.6],
              opacityTo: [0.3, 0.3],
              stops: [0, 100],
            },
          },
          markers: {
            colors: [color1, color2],
            strokeWidth: 3,
            size: 0,
            hover: { size: 10 },
          },
          xaxis: {
            categories: [
              'Jan', 'Feb', 'Mar', 'Apr', 'May',
              'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
            ],
            tooltip: { enabled: false },
            labels: {
              formatter: value => value,
              style: { fontSize: '14px' },
            },
          },
          yaxis: {
            min:0,
            max:70,
            labels: {
              formatter: value => `$${value}k`,
              style: { fontSize: '14px' },
            },
          },
          tooltip: {
            x: { format: 'dd/MM/yy HH:mm' },
          },
        };
  
        const chart = new ApexCharts(document.querySelector(`#${chartId}`), options);
        chart.render();
      },
    },
  };
  </script>
  