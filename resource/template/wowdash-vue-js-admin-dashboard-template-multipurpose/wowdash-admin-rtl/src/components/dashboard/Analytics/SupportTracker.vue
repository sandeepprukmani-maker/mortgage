<template>
    <div class="col-xxl-4 col-xl-6">
      <div class="card h-100">
        <div class="card-body p-24">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
            <h6 class="mb-2 fw-bold text-lg">Support Tracker</h6>
            <select class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8">
              <option>Yearly</option>
              <option>Monthly</option>
              <option>Weekly</option>
              <option>Today</option>
            </select>
          </div>
          <div class="mt-32 d-flex flex-wrap gap-24 align-items-center justify-content-between">
            <div class="d-flex flex-column gap-24">
              <div class="d-flex align-items-center gap-3">
                <div class="w-40-px h-40-px rounded-circle d-flex justify-content-center align-items-center bg-primary-100 flex-shrink-0">
                  <img src="@/assets/images/home-nine/ticket1.png" alt="" class="">
                </div>
                <div class="flex-grow-1">
                  <h6 class="text-md mb-0 fw-bold">172</h6>
                  <span class="text-sm text-secondary-light fw-normal">New Tickets</span>
                </div>
              </div>
              <div class="d-flex align-items-center gap-3">
                <div class="w-40-px h-40-px rounded-circle d-flex justify-content-center align-items-center bg-warning-100 flex-shrink-0">
                  <img src="@/assets/images/home-nine/ticket2.png" alt="" class="">
                </div>
                <div class="flex-grow-1">
                  <h6 class="text-md mb-0 fw-bold">172</h6>
                  <span class="text-sm text-secondary-light fw-normal">Open Tickets</span>
                </div>
              </div>
              <div class="d-flex align-items-center gap-3">
                <div class="w-40-px h-40-px rounded-circle d-flex justify-content-center align-items-center bg-lilac-100 flex-shrink-0">
                  <img src="@/assets/images/home-nine/ticket3.png" alt="" class="">
                </div>
                <div class="flex-grow-1">
                  <h6 class="text-md mb-0 fw-bold">172</h6>
                  <span class="text-sm text-secondary-light fw-normal">Response Time</span>
                </div>
              </div>
            </div>
            <div class="position-relative">
              <div id="userOverviewDonutChart" class="apexcharts-tooltip-z-none"></div>
              <div class="text-center max-w-135-px max-h-135-px bg-warning-focus rounded-circle p-16 aspect-ratio-1 d-flex flex-column justify-content-center align-items-center position-absolute start-50 top-50 translate-middle">
                <h6 class="fw-bold">120</h6>
                <span class="text-secondary-light">Total Tickets</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts';
  
  export default {
    name: 'SupportTracker',
    mounted() {
      this.createDonutChart();
    },
    methods: {
      createDonutChart() {
        const options = {
          series: [500, 500, 500],
          colors: ['#FF9F29', '#487FFF', '#45B369'],
          labels: ['Active', 'New', 'Total'],
          legend: {
            show: false,
          },
          chart: {
            type: 'donut',
            height: 270,
            sparkline: {
              enabled: true, // Remove whitespace
            },
            margin: {
              top: 0,
              right: 0,
              bottom: 0,
              left: 0,
            },
            padding: {
              top: 0,
              right: 0,
              bottom: 0,
              left: 0,
            },
          },
          stroke: {
            width: 0,
          },
          dataLabels: {
            enabled: false,
          },
          responsive: [
            {
              breakpoint: 480,
              options: {
                chart: {
                  width: 200,
                },
                legend: {
                  position: 'bottom',
                },
              },
            },
          ],
        };
  
        var chart = new ApexCharts(
          document.querySelector('#userOverviewDonutChart'),
          options
        );
        chart.render();
      },
    },
  };
  </script>