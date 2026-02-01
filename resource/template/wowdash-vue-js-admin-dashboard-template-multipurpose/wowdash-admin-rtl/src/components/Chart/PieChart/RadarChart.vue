<template>
    <div class="col-md-6">
      <div class="card h-100 p-0">
        <div class="card-header border-bottom bg-base py-16 px-24">
          <h6 class="text-lg fw-semibold mb-0">Radar Chart</h6>
        </div>
        <div class="card-body p-24 text-center">
          <div id="radarChart" class="square-marker check-marker series-gap-24 d-flex justify-content-center"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from "apexcharts";
  
  export default {
    name: "RadarChart",
    mounted() {
      this.renderChart();
    },
    methods: {
      renderChart() {
        const options = {
          series: [{
            name: 'Product 1',
            data: [80, 50, 30, 40, 60, 20, 62, 30, 40, 80],
          }, {
            name: 'Product 2',
            data: [80, 60, 80, 70, 68, 60, 56, 50, 40, 45],
          }],
          colors: ['#FF9F29', '#487FFF'],
          chart: {
            height: 264,
            type: 'radar',
            toolbar: {
              show: false,
            },
            dropShadow: {
              enabled: true,
              blur: 1,
              left: 1,
              top: 1
            }
          },
          stroke: {
            width: 2
          },
          fill: {
            opacity: 0.25
          },
          markers: {
            size: 0
          },
          yaxis: {
            stepSize: 20
          },
          xaxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul']
          }
        };
  
        const chart = new ApexCharts(document.querySelector("#radarChart"), options);
        chart.render();
      },
    },
  };
  </script>