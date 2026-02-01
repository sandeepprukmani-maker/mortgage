<template>
    <div class="col-md-6">
      <div class="card h-100 p-0">
        <div class="card-header border-bottom bg-base py-16 px-24">
          <h6 class="text-lg fw-semibold mb-0">Basic Pie Chart</h6>
        </div>
        <div class="card-body p-24 text-center">
          <div id="pieChart" class="d-flex justify-content-center apexcharts-tooltip-z-none"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from "apexcharts";
  
  export default {
    name: "BasicPieChart",
    mounted() {
      this.renderChart();
    },
    methods: {
      renderChart() {
        const options = {
          series: [70, 80, 90, 30],
          chart: {
            height: 264,
            type: 'pie',
          },
          stroke: {
            show: false, // This will remove the white border
          },
          labels: ['Team A', 'Team B', 'Team C', 'Team D'],
          colors: ['#487FFF', "#FF9F29", '#45B369', '#EF4A00'],
          plotOptions: {
            pie: {
              dataLabels: {
                dropShadow: {
                  enabled: true,
                },
              },
            },
          },
          legend: {
            position: 'bottom',
            horizontalAlign: 'center', // Align the legend horizontally
          },
          responsive: [{
            breakpoint: 480,
            options: {
              chart: {
                width: 200
              },
              legend: {
                show: false,
                position: 'bottom', // Ensure the legend is at the bottom
                horizontalAlign: 'center', // Align the legend horizontally
                offsetX: -10,
                offsetY: 0
              }
            }
          }]
        };
        const chart = new ApexCharts(document.querySelector("#pieChart"), options);
        chart.render();
      },
    },
  };
  </script>