<template>
    <div class="col-md-6">
      <div class="card h-100 p-0">
        <div class="card-header border-bottom bg-base py-16 px-24">
          <h6 class="text-lg fw-semibold mb-0">Line Chart with Data Labels</h6>
        </div>
        <div class="card-body p-24">
          <div id="lineDataLabel"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts'
  
  export default {
    name: 'LineDataLabelChart',
    mounted() {
      this.renderChart();
    },
    methods: {
      renderChart() {
        const options = {
          series: [{
            name: "Desktops",
            data: [5, 25, 35, 15, 21, 15, 35, 35, 51]
          }],
          chart: {
            height: 264,
            type: 'line',
            colors: '#000',
            zoom: {
              enabled: false
            },
            toolbar: {
              show: false
            }
          },
          colors: ['#487FFF'],
          dataLabels: {
            enabled: true
          },
          stroke: {
            curve: 'straight',
            width: 4,
            color: "#000"
          },
          markers: {
            colors: '#487FFF',
            strokeWidth: 3,
            size: 0,
            hover: {
              size: 10
            }
          },
          grid: {
            show: true,
            borderColor: '#D1D5DB',
            strokeDashArray: 3,
            row: {
              colors: ['#f3f3f3', 'transparent'],
              opacity: 0
            }
          },
          xaxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            lines: {
              show: false
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
  
        const chart = new ApexCharts(document.querySelector("#lineDataLabel"), options);
        chart.render();
      }
    }
  }
  </script>
  