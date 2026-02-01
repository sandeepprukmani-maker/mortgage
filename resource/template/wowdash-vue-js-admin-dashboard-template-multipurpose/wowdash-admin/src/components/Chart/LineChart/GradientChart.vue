<template>
    <div class="col-md-6">
      <div class="card h-100 p-0">
        <div class="card-header border-bottom bg-base py-16 px-24">
          <h6 class="text-lg fw-semibold mb-0">Gradient Charts</h6>
        </div>
        <div class="card-body p-24">
          <div id="gradientLineChart"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts';
  
  export default {
    name: 'GradientLineChart',
    mounted() {
      this.renderChart();
    },
    methods: {
      renderChart() {
        const options = {
          series: [{
            name: "This month",
            data: [12, 6, 22, 18, 38, 16, 40, 8, 35, 18, 35, 22, 50]
          }],
          chart: {
            height: 264,
            type: 'line',
            toolbar: {
              show: false
            },
            zoom: {
              enabled: false
            },
          },
          dataLabels: {
            enabled: false
          },
          stroke: {
            curve: 'smooth',
            colors: ['#FF9F29'],
            width: 4
          },
          fill: {
            type: 'gradient',
            gradient: {
              shade: 'dark',
              gradientToColors: ['#0E53F4'],
              shadeIntensity: 1,
              type: 'horizontal',
              opacityFrom: 1,
              opacityTo: 1,
              stops: [0, 100, 100, 100]
            },
          },
          markers: {
            size: 0,
            strokeWidth: 3,
            hover: {
              size: 8
            }
          },
          tooltip: {
            enabled: true,
            x: { show: true },
            y: { show: false },
            z: { show: false }
          },
          grid: {
            row: {
              colors: ['transparent', 'transparent'],
              opacity: 0.5
            },
            borderColor: '#D1D5DB',
            strokeDashArray: 3,
          },
          yaxis: {
            labels: {
              formatter: function (value) {
                return "$" + value + "k";
              },
              style: {
                fontSize: "14px"
              }
            }
          },
          xaxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            tooltip: {
              enabled: false
            },
            labels: {
              formatter: function (value) {
                return value;
              },
              style: {
                fontSize: "14px"
              }
            },
            axisBorder: {
              show: false
            }
          }
        };
  
        const chart = new ApexCharts(document.querySelector("#gradientLineChart"), options);
        chart.render();
      }
    }
  }
  </script>
  