<template>
    <div class="col-md-6">
      <div class="card h-100 p-0">
        <div class="card-header border-bottom bg-base py-16 px-24">
          <h6 class="text-lg fw-semibold mb-0">Default Line Chart</h6>
        </div>
        <div class="card-body p-24">
          <div id="defaultLineChart" class="apexcharts-tooltip-style-1"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts'
  
  export default {
    name: 'DefaultLineChart',
    mounted() {
      this.renderChart()
    },
    methods: {
      renderChart() {
        const options = {
          series: [{
            name: "This month",
            data: [0, 48, 20, 24, 6, 33, 30, 48, 35, 18, 20, 5]
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
            colors: ['#487FFF'],
            width: 4
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
            x: {
              show: true,
            },
            y: {
              show: false,
            },
            z: {
              show: false,
            }
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
            },
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
            },
            // Uncomment to enable crosshairs
            // crosshairs: {
            //   show: true,
            //   width: 20,
            //   stroke: {
            //     width: 0
            //   },
            //   fill: {
            //     type: 'solid',
            //     color: '#487FFF40',
            //   }
            // }
          }
        };
  
        const chart = new ApexCharts(document.querySelector("#defaultLineChart"), options);
        chart.render();
      }
    }
  }
  </script>
  