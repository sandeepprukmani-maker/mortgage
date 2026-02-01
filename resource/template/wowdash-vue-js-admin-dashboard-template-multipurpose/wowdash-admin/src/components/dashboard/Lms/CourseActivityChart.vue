<template>
  <div class="col-xxl-4">
    <div class="card h-100">
      <div class="card-header">
        <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
          <h6 class="mb-2 fw-bold text-lg mb-0">Course Activity</h6>
          <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
            View All
            <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
          </a>
        </div>
      </div>
      <div class="card-body p-24">
        <ul class="d-flex flex-wrap align-items-center justify-content-center my-3 gap-3">
          <li class="d-flex align-items-center gap-2">
            <span class="w-12-px h-12-px rounded-circle bg-warning-600"></span>
            <span class="text-secondary-light text-sm fw-semibold">
              Paid Course:
              <span class="text-primary-light fw-bold">500</span>
            </span>
          </li>
          <li class="d-flex align-items-center gap-2">
            <span class="w-12-px h-12-px rounded-circle bg-success-main"></span>
            <span class="text-secondary-light text-sm fw-semibold">
              Free Course:
              <span class="text-primary-light fw-bold">300</span>
            </span>
          </li>
        </ul>
        <div id="paymentStatusChart" class="margin-16-minus y-value-left"></div>
      </div>
    </div>
  </div>
</template>

<script>
import ApexCharts from 'apexcharts';

export default {
  name: 'CourseActivityChart',
  mounted() {
    const options = {
      series: [
        {
          name: 'Net Profit',
          data: [44, 100, 40, 56, 30, 58, 50]
        },
        {
          name: 'Free Cash',
          data: [60, 120, 60, 90, 50, 95, 90]
        }
      ],
      colors: ['#45B369', '#FF9F29'],
      labels: ['Active', 'New', 'Total'],
      legend: {
        show: false
      },
      chart: {
        type: 'bar',
        height: 420,
        toolbar: {
          show: false
        }
      },
      grid: {
        show: true,
        borderColor: '#D1D5DB',
        strokeDashArray: 4,
        position: 'back'
      },
      plotOptions: {
        bar: {
          borderRadius: 4,
          columnWidth: 8
        }
      },
      dataLabels: {
        enabled: false
      },
      states: {
        hover: {
          filter: {
            type: 'none'
          }
        }
      },
      stroke: {
        show: true,
        width: 0,
        colors: ['transparent']
      },
      yaxis: {
        min: 0,
        max: 120,
        tickAmount: 4,
      },
      xaxis: {
        categories: ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
      },
      fill: {
        opacity: 1,
        width: 18
      }
    };

    const chart = new ApexCharts(document.querySelector("#paymentStatusChart"), options);
    chart.render();
  }
};
</script>
