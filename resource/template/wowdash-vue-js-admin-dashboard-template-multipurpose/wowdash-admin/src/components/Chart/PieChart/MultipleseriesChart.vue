<template>
    <div class="col-md-6">
      <div class="card h-100 p-0">
        <div class="card-header border-bottom bg-base py-16 px-24">
          <h6 class="text-lg fw-semibold mb-0">Multiple series</h6>
        </div>
        <div class="card-body p-24 text-center">
          <div id="multipleSeriesChart" class="apexcharts-tooltip-z-none square-marker check-marker series-gap-24 d-flex justify-content-center"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from "apexcharts";
  
  export default {
    name: "MultipleSeriesChart",
    mounted() {
      this.renderChart();
    },
    methods: {
      renderChart() {
        const options = {
          series: [20, 22, 28, 10],
          chart: {
            type: 'polarArea',
            height: 264,
          },
          labels: ['Product 1', 'Product 2', 'Product 3', 'Product 4'],
          colors: ['#487FFF', '#FF9F29', '#9935FE', '#EF4A00'],
          stroke: {
            colors: ['#487FFF', '#FF9F29', '#9935FE', '#EF4A00'],
          },
          fill: {
            opacity: 0.8
          },
          legend: {
            position: 'bottom',
            horizontalAlign: 'center' // Align the legend horizontally
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
  
        const chart = new ApexCharts(document.querySelector("#multipleSeriesChart"), options);
        chart.render();
      },
    },
  };
  </script>