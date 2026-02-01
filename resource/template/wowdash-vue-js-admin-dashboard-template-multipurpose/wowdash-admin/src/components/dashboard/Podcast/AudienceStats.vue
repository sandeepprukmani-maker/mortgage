<template>
    <div class="col-xxl-8 col-lg-7">
      <div class="bg-base radius-12 py-20 px-24 shadow-9 h-100">
        <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
          <h6 class="mb-0 fw-bold text-lg">Audience Stats</h6>
          <select class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8">
            <option>Yearly</option>
            <option>Monthly</option>
            <option>Weekly</option>
            <option>Today</option>
          </select>
        </div>
        <ul class="d-flex flex-wrap align-items-center justify-content-center mt-18 gap-3">
          <li class="d-flex align-items-center gap-2">
            <span class="w-10-px h-6-px rounded-pill bg-primary-600"></span>
            <span class="text-secondary-light text-sm fw-medium d-inline-flex align-items-center gap-1">
              Total Audience:
              <span class="text-primary-light text-xl fw-bold">26,201</span>
            </span>
          </li>
        </ul>
        <div class="mt-24">
          <div id="paymentStatusChart" ref="chartContainer"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts';
  
  export default {
    name: 'AudienceStatsChart',
    mounted() {
      const options = {
        series: [
          {
            name: 'Net Profit',
            data: [44, 100, 40, 56, 30, 58, 50, 44, 100, 40, 56, 30],
          },
          {
            name: 'Revenue',
            data: [90, 140, 80, 125, 70, 140, 110, 90, 140, 80, 125, 70],
          },
          {
            name: 'Free Cash',
            data: [60, 120, 60, 90, 50, 95, 90, 60, 120, 60, 90, 50],
          },
        ],
        colors: ['#E4F1FF', '#E4F1FF', '#E4F1FF'],
        labels: ['Active', 'New', 'Total'],
        legend: {
          show: false,
        },
        chart: {
          type: 'bar',
          height: 300,
          toolbar: {
            show: false,
          },
        },
        grid: {
          show: true,
          borderColor: '#00000000',
          strokeDashArray: 4,
          position: 'back',
        },
        plotOptions: {
          bar: {
            borderRadius: 2,
            columnWidth: '70%',
            borderRadiusApplication: 'end',
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
          width: 4,
          colors: ['transparent'],
        },
        xaxis: {
          categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        },
        yaxis: {
          min:0,
          max:160,
          categories: ['0', '10,000', '20,000', '30,000', '50,000', '1,00,000', '1,00,000'],
          labels: {
            formatter: function (value) {
              return '$' + value + 'k';
            },
            style: {
              fontSize: '14px',
            },
          },
        },
        fill: {
          opacity: 1,
          width: 18,
        },
      };
  
      const chart = new ApexCharts(this.$refs.chartContainer, options);
      chart.render();
    },
  };
  </script>
  