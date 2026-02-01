<template>
    <div class="col-xxl-3 col-xl-6">
      <div class="card h-100 radius-8 border">
        <div class="card-body p-24">
          <h6 class="mb-12 fw-semibold text-lg mb-16">Total Subscriber</h6>
          <div class="d-flex align-items-center gap-2 mb-20">
            <h6 class="fw-semibold mb-0">5,000</h6>
            <p class="text-sm mb-0">
              <span
                class="bg-danger-focus border br-danger px-8 py-2 rounded-pill fw-semibold text-danger-main text-sm d-inline-flex align-items-center gap-1"
              >
                10%
                <iconify-icon
                  icon="iconamoon:arrow-down-2-fill"
                  class="icon"
                ></iconify-icon>
              </span>
              - 20 Per Day
            </p>
          </div>
  
          <div id="barChart"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts';
  import { onMounted } from 'vue';
  
  export default {
    name: 'TotalSubscriber',
    setup() {
      onMounted(() => {
        var options = {
          series: [
            {
              name: 'Sales',
              data: [
                { x: 'Sun', y: 15 },
                { x: 'Mon', y: 12 },
                { x: 'Tue', y: 18 },
                { x: 'Wed', y: 20 },
                { x: 'Thu', y: 13 },
                { x: 'Fri', y: 16 },
                { x: 'Sat', y: 6 },
              ],
            },
          ],
          chart: {
            type: 'bar',
            height: 235,
            toolbar: {
              show: false,
            },
          },
          plotOptions: {
            bar: {
              borderRadius: 6,
              horizontal: false,
              columnWidth: '52%',
              endingShape: 'rounded',
            },
          },
          dataLabels: {
            enabled: false,
          },
          fill: {
            type: 'gradient',
            colors: ['#dae5ff'],
            gradient: {
              shade: 'light',
              type: 'vertical',
              shadeIntensity: 0.5,
              gradientToColors: ['#dae5ff'],
              inverseColors: false,
              opacityFrom: 1,
              opacityTo: 1,
              stops: [0, 100],
            },
          },
          grid: {
            show: false,
            borderColor: '#D1D5DB',
            strokeDashArray: 4,
            position: 'back',
            padding: {
              top: -10,
              right: -10,
              bottom: -10,
              left: -10,
            },
          },
          xaxis: {
            type: 'category',
            categories: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
          },
          yaxis: {
            show: false,
          },
        };
  
        var chart = new ApexCharts(document.querySelector("#barChart"), options);
        chart.render();
      });
    },
  };
  </script>