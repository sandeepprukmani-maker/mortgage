<template>
    <div class="col-md-6">
      <div class="card h-100 p-0">
        <div class="card-header border-bottom bg-base py-16 px-24">
          <h6 class="text-lg fw-semibold mb-0">Line Chart Animation</h6>
        </div>
        <div class="card-body p-24">
          <div id="doubleLineChart"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts';
  
  export default {
    name: 'DoubleLineChart',
    mounted() {
      this.createLineChart('doubleLineChart', '#487fff');
    },
    methods: {
      createLineChart(chartId, chartColor) {
        const options = {
          series: [
            {
              name: 'This Day',
              data: [8, 15, 9, 20, 10, 33, 13, 22, 8, 17, 10, 15],
            },
            {
              name: 'Example',
              data: [8, 24, 18, 40, 18, 48, 22, 38, 18, 30, 20, 28],
            },
          ],
          chart: {
            type: 'line',
            width: '100%',
            height: 264,
            sparkline: {
              enabled: false
            },
            toolbar: {
              show: false
            },
            padding: {
              left: 0,
              right: 0,
              top: 0,
              bottom: 0
            }
          },
          colors: ['#487FFF', '#FF9F29'],
          dataLabels: {
            enabled: false
          },
          stroke: {
            curve: 'smooth',
            width: 4,
            colors: ["#FF9F29", chartColor],
            lineCap: 'round',
          },
          grid: {
            show: true,
            borderColor: '#D1D5DB',
            strokeDashArray: 3,
            position: 'back',
            xaxis: {
              lines: {
                show: false
              }
            },
            yaxis: {
              lines: {
                show: true
              }
            },
            row: {
              colors: undefined,
              opacity: 0.5
            },
            column: {
              colors: undefined,
              opacity: 0.5
            },
            padding: {
              top: 0,
              right: 0,
              bottom: 0,
              left: 0
            }
          },
          markers: {
            colors: ["#FF9F29", chartColor],
            strokeWidth: 3,
            size: 0,
            hover: {
              size: 10
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
            }
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
          tooltip: {
            x: {
              format: 'dd/MM/yy HH:mm'
            }
          },
          legend: {
            show: false
          }
        };
  
        const chart = new ApexCharts(document.querySelector(`#${chartId}`), options);
        chart.render();
      }
    }
  }
  </script>
  