<template>
    <div class="col-xxl-4 col-md-6">
      <div class="shadow-7 radius-12 bg-base h-100 overflow-hidden">
        <div class="card-header border-bottom bg-base py-16 px-24 d-flex align-items-center justify-content-between">
          <h6 class="text-lg fw-semibold mb-0">Top 5 Categories</h6>
          <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
            View All
            <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
          </a>
        </div>
        <div class="card-body p-32 mt-20 d-flex align-items-center justify-content-between gap-24">
          <div>
            <apexchart
              id="userOverviewDonutChart"
              class="margin-16-minus y-value-left apexcharts-tooltip-z-none"
              type="donut"
              :options="chartOptions"
              :series="series"
              height="270"
            ></apexchart>
          </div>
          <ul class="d-flex flex-column gap-12">
            <li><span class="text-lg">UI/UX Design: <span class="text-success-600 fw-semibold">50%</span></span></li>
            <li><span class="text-lg">Entertainment: <span class="text-purple fw-semibold">30%</span></span></li>
            <li><span class="text-lg">Lifestyle: <span class="text-danger-600 fw-semibold">87%</span></span></li>
            <li><span class="text-lg">Business: <span class="text-primary-600 fw-semibold">87%</span></span></li>
            <li><span class="text-lg">Health: <span class="text-warning-600 fw-semibold">40%</span></span></li>
          </ul>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts';
  import VueApexCharts from 'vue3-apexcharts';
  
  export default {
    name: 'TopCategories',
    components: {
      apexchart: VueApexCharts,
    },
    data() {
      return {
        series: [40, 87, 87, 30, 50],
        chartOptions: {
          chart: {
            type: 'donut',
            height: 270,
            sparkline: { enabled: true },
            margin: { top: 0, right: 0, bottom: 0, left: 0 },
            padding: { top: 0, right: 0, bottom: 0, left: 0 },
          },
          colors: ['#FF9F29', '#487FFF', '#EF4A00', '#9935FE', '#45B369'],
          labels: ['Health', 'Business', 'Lifestyle', 'Entertainment', 'UI/UX Design'],
          stroke: { width: 0 },
          dataLabels: { enabled: false },
          legend: { show: false },
          responsive: [
            {
              breakpoint: 480,
              options: {
                chart: { width: 200 },
                legend: { position: 'bottom' },
              },
            },
          ],
        },
      };
    },
  };
  </script>
  