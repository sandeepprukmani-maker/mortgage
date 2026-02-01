<template>
    <div class="col-xxl-4 col-lg-6">
      <div class="card h-100 border shadow-none radius-8 overflow-hidden">
        <div class="card-body p-24">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
            <h6 class="mb-2 fw-bold text-lg">Users Overview</h6>
            <div>
              <select class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8">
                <option>Today</option>
                <option>Weekly</option>
                <option>Monthly</option>
                <option>Yearly</option>
              </select>
            </div>
          </div>
  
          <apexchart
            type="donut"
            height="270"
            :options="chartOptions"
            :series="chartSeries"
          />
  
          <ul class="d-flex flex-wrap align-items-center justify-content-between mt-3 gap-3">
            <li class="d-flex align-items-center gap-2">
              <span class="w-12-px h-12-px radius-2 bg-primary-600"></span>
              <span class="text-secondary-light text-sm fw-normal">
                New:
                <span class="text-primary-light fw-semibold">500</span>
              </span>
            </li>
            <li class="d-flex align-items-center gap-2">
              <span class="w-12-px h-12-px radius-2 bg-yellow"></span>
              <span class="text-secondary-light text-sm fw-normal">
                Subscribed:
                <span class="text-primary-light fw-semibold">300</span>
              </span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { defineComponent } from 'vue';
  import VueApexCharts from 'vue3-apexcharts';
  
  export default defineComponent({
    name: 'UserOverviewDonutChart',
    components: {
      apexchart: VueApexCharts,
    },
    data() {
      return {
        chartSeries: [500, 500, 500],
        chartOptions: {
          chart: {
            type: 'donut',
            height: 270,
            sparkline: {
              enabled: true,
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
          labels: ['Active', 'New', 'Total'],
          colors: ['#FF9F29', '#487FFF', '#E4F1FF'],
          legend: {
            show: false,
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
        },
      };
    },
  });
  </script>
  