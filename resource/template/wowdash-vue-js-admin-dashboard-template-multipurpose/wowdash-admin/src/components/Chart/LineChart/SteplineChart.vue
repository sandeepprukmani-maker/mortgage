<template>
    <div class="col-md-6">
      <div class="card h-100 p-0">
        <div class="card-header border-bottom bg-base py-16 px-24">
          <h6 class="text-lg fw-semibold mb-0">Stepline Charts</h6>
        </div>
        <div class="card-body p-24">
          <div id="stepLineChart"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts';
  
  export default {
    name: 'StepLineChart',
    mounted() {
      this.renderChart();
    },
    methods: {
      renderChart() {
        const options = {
          series: [
            {
              data: [16, 25, 38, 50, 32, 20, 42, 18, 4, 25, 12, 12],
              name: "Example",
            },
          ],
          chart: {
            type: 'line',
            height: 270,
            toolbar: {
              show: false
            },
          },
          stroke: {
            curve: 'stepline',
          },
          colors: ['#487FFF'],
          dataLabels: {
            enabled: false
          },
          markers: {
            hover: {
              sizeOffset: 4
            }
          },
          grid: {
            show: true,
            borderColor: '#D1D5DB',
            strokeDashArray: 3,
            position: 'back',
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
          }
        };
  
        const chart = new ApexCharts(document.querySelector("#stepLineChart"), options);
        chart.render();
      }
    }
  }
  </script>
  