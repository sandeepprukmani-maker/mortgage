<template>
    <div class="col-xxl-4 col-sm-6">
      <div class="shadow-7 radius-12 bg-base h-100 overflow-hidden">
        <div class="card-header border-bottom bg-base py-16 px-24 d-flex align-items-center justify-content-between">
          <h6 class="text-lg fw-semibold mb-0">Tasks Overview</h6>
          <div>
            <select class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8">
              <option>Yearly</option>
              <option>Monthly</option>
              <option>Weekly</option>
              <option>Today</option>
            </select>
          </div>
        </div>
        <div class="card-body p-32 mt-20">
          <div class="position-relative text-center">
            <div id="taskOverviewChart" class="margin-16-minus y-value-left apexcharts-tooltip-z-none"></div>
            <div class="text-center position-absolute top-50 start-50 translate-middle">
              <span class="text-secondary-light">Total Tasks</span>
              <h6 class="mb-0 mt-1">46</h6>
            </div>
          </div>
        </div>
        <ul class="d-flex flex-wrap align-items-center justify-content-center pb-24 mt-24 gap-28">
          <li class="d-flex align-items-center gap-2">
            <span class="w-12-px h-12-px rounded-circle bg-warning-main"></span>
            <span class="text-secondary-light text-sm fw-medium">Pending</span>
          </li>
          <li class="d-flex align-items-center gap-2">
            <span class="w-12-px h-12-px rounded-circle bg-info-main"></span>
            <span class="text-secondary-light text-sm fw-medium">In Progress</span>
          </li>
          <li class="d-flex align-items-center gap-2">
            <span class="w-12-px h-12-px rounded-circle bg-purple"></span>
            <span class="text-secondary-light text-sm fw-medium">Completed</span>
          </li>
          <li class="d-flex align-items-center gap-2">
            <span class="w-12-px h-12-px rounded-circle bg-danger"></span>
            <span class="text-secondary-light text-sm fw-medium">Cancelled</span>
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts'
  
  export default {
    name: 'TasksOverview',
    mounted() {
      const options = {
        series: [40, 87, 87, 30],
        colors: ['#dc3545', '#ff9f29', '#8252e9', '#144bd6'],
        labels: ['Health', 'Business', 'Lifestyle', 'Entertainment'],
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
          width: 2
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
  
      const chart = new ApexCharts(document.querySelector("#taskOverviewChart"), options);
      chart.render();
    }
  }
  </script>