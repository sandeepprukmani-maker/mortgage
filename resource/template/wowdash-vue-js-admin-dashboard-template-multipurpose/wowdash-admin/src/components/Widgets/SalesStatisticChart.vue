<template>
  <div class="col-xxl-6 col-xl-12">
    <div class="card h-100">
      <div class="card-body">
        <div class="d-flex flex-wrap align-items-center justify-content-between">
          <h6 class="text-lg mb-0">Sales Statistic</h6>
          <select class="form-select bg-base form-select-sm w-auto radius-8">
            <option>Yearly</option>
            <option>Monthly</option>
            <option>Weekly</option>
            <option>Today</option>
          </select>
        </div>
        <div class="d-flex flex-wrap align-items-center gap-2 mt-8">
          <h6 class="mb-0">$27,200</h6>
          <span
            class="text-sm fw-semibold rounded-pill bg-success-focus text-success-main border br-success px-8 py-4 line-height-1 d-flex align-items-center gap-1"
          >
            10% <iconify-icon icon="bxs:up-arrow" class="text-xs"></iconify-icon>
          </span>
          <span class="text-xs fw-medium">+ $1500 Per Day</span>
        </div>
        <div id="chart" class="pt-28 apexcharts-tooltip-style-1"></div>
      </div>
    </div>
  </div>
</template>

<script>
import ApexCharts from 'apexcharts';
import { onMounted } from 'vue';

export default {
  name: 'SalesStatistic',
  setup() {
    onMounted(() => {
      var options = {
        series: [
          {
            name: 'This month',
            data: [10, 20, 12, 30, 14, 35, 16, 32, 14, 25, 13, 28],
          },
        ],
        chart: {
          height: 264,
          type: 'line',
          toolbar: {
            show: false,
          },
          zoom: {
            enabled: false,
          },
          dropShadow: {
            enabled: true,
            top: 6,
            left: 0,
            blur: 4,
            color: '#000',
            opacity: 0.1,
          },
        },
        colors: ['#487FFF'],
        dataLabels: {
          enabled: false,
        },
        stroke: {
          curve: 'smooth',
          colors: ['#487FFF'],
          width: 3,
        },
        markers: {
          size: 0,
          strokeWidth: 3,
          hover: {
            size: 8,
          },
        },
        tooltip: {
          enabled: true,
          x: {
            show: true,
          },
          y: {
            show: false,
          },
          z: {
            show: false,
          },
        },
        grid: {
          row: {
            colors: ['transparent', 'transparent'],
            opacity: 0.5,
          },
          borderColor: '#D1D5DB',
          strokeDashArray: 3,
        },
        yaxis: {
          min:6,
          max:36,
          tickAmount:5,
          labels: {
            formatter: function (value) {
              return '$' + value + 'k';
            },
            style: {
              fontSize: '14px',
            },
          },
        },
        xaxis: {
          categories: [
            'Jan',
            'Feb',
            'Mar',
            'Apr',
            'May',
            'Jun',
            'Jul',
            'Aug',
            'Sep',
            'Oct',
            'Nov',
            'Dec',
          ],
          tooltip: {
            enabled: false,
          },
          labels: {
            formatter: function (value) {
              return value;
            },
            style: {
              fontSize: '14px',
            },
          },
          axisBorder: {
            show: false,
          },
          crosshairs: {
            show: true,
            width: 20,
            stroke: {
              width: 0,
            },
            fill: {
              type: 'solid',
              color: '#487FFF40',
            },
          },
        },
      };

      var chart = new ApexCharts(document.querySelector('#chart'), options);
      chart.render();
    });
  },
};
</script>