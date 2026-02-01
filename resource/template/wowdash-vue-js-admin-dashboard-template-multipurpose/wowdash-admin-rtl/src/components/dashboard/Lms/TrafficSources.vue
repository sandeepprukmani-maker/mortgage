<template>
  <div class="col-xxl-4 col-md-6">
    <div class="card h-100 radius-8 border-0">
      <div class="card-body p-24 d-flex flex-column justify-content-between gap-8">
        <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between mb-20">
          <h6 class="mb-2 fw-bold text-lg mb-0">Traffic Sources</h6>
          <select class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8">
            <option>Yearly</option>
            <option>Monthly</option>
            <option>Weekly</option>
            <option>Today</option>
          </select>
        </div>
        <div id="userOverviewDonutChart" class="margin-16-minus y-value-left apexcharts-tooltip-z-none"></div>

        <ul class="d-flex flex-wrap align-items-center justify-content-between mt-3 gap-3">
          <li class="d-flex flex-column gap-8">
            <div class="d-flex align-items-center gap-2">
              <span class="w-12-px h-12-px rounded-circle bg-warning-600"></span>
              <span class="text-secondary-light text-sm fw-semibold">Organic Search</span>
            </div>
            <span class="text-primary-light fw-bold">875</span>
          </li>
          <li class="d-flex flex-column gap-8">
            <div class="d-flex align-items-center gap-2">
              <span class="w-12-px h-12-px rounded-circle bg-success-600"></span>
              <span class="text-secondary-light text-sm fw-semibold">Referrals</span>
            </div>
            <span class="text-primary-light fw-bold">450</span>
          </li>
          <li class="d-flex flex-column gap-8">
            <div class="d-flex align-items-center gap-2">
              <span class="w-12-px h-12-px rounded-circle bg-primary-600"></span>
              <span class="text-secondary-light text-sm fw-semibold">Social Media</span>
            </div>
            <span class="text-primary-light fw-bold">4,305</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import ApexCharts from 'apexcharts';

export default {
  name: 'UserOverviewDonutChart',
  mounted() {
    const options = {
      series: [500, 500, 500],
      colors: ['#FF9F29', '#487FFF', '#E4F1FF'],
      labels: ['Active', 'New', 'Total'],
      legend: {
        show: false
      },
      chart: {
        type: 'donut',
        height: 270,
        sparkline: {
          enabled: true
        },
        margin: {
          top: 0,
          right: 0,
          bottom: 0,
          left: 0
        },
        padding: {
          top: 0,
          right: 0,
          bottom: 0,
          left: 0
        }
      },
      stroke: {
        width: 0
      },
      dataLabels: {
        enabled: false
      },
      responsive: [{
        breakpoint: 480,
        options: {
          chart: {
            width: 200
          },
          legend: {
            position: 'bottom'
          }
        }
      }]
    };

    const chart = new ApexCharts(document.querySelector("#userOverviewDonutChart"), options);
    chart.render();
  }
};
</script>
