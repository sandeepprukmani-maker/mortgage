<template>
    <div class="col-lg-4">
      <div class="shadow-7 p-0 radius-12 bg-base overflow-hidden h-100">
        <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between py-12 px-20 border-bottom border-neutral-200">
          <h6 class="mb-0 fw-bold text-lg">Ticket Status</h6>
          <div>
            <select class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8">
              <option>Yearly</option>
              <option>Monthly</option>
              <option>Weekly</option>
              <option>Today</option>
            </select>
          </div>
        </div>
        <div class="card-body p-20">
          <div id="multipleSeriesChart" class="apexcharts-tooltip-z-none square-marker check-marker series-gap-24 d-flex justify-content-center"></div>
          <div class="d-flex align-items-center gap-3 text-sm justify-content-center mt-3">
            <span class="text-secondary-light fw-medium">Pending: <span class="fw-semibold text-warning-600">32</span></span>
            <span class="text-secondary-light fw-medium">Hold: <span class="fw-semibold text-purple">10</span></span>
            <span class="text-secondary-light fw-medium">Complete: <span class="fw-semibold text-success-600">25</span></span>
            <span class="text-secondary-light fw-medium">Cancelled: <span class="fw-semibold text-danger-600">28</span></span>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts';
  
  export default {
    name: 'TicketStatus',
    mounted() {
      const options = {
        series: [20, 22, 28, 10],
        chart: {
          type: 'polarArea',
          height: 240
        },
        labels: ['Product 1', 'Product 2', 'Product 3', 'Product 4'],
        colors: ['#487FFF', '#FF9F29', '#9935FE', '#EF4A00'],
        stroke: {
          colors: ['#487FFF', '#FF9F29', '#9935FE', '#EF4A00']
        },
        fill: {
          opacity: 0.8
        },
        legend: {
          show: false,
          position: 'bottom',
          horizontalAlign: 'center'
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
        }], 
        yaxis: {
        min: 0,
        max: 30,
        tickAmount: 5,
      }
      };
  
      const chart = new ApexCharts(document.querySelector("#multipleSeriesChart"), options);
      chart.render();
    }
  };
  </script>
  