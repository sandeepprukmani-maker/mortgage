<template>
    <div class="col-md-6">
      <div class="card h-100 p-0">
        <div class="card-header border-bottom bg-base py-16 px-24">
          <h6 class="text-lg fw-semibold mb-0">Column Charts</h6>
        </div>
        <div class="card-body p-24">
          <div id="columnGroupBarChart"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts';
  
  export default {
    name: 'ColumnGroupBarChart',
    mounted() {
      this.renderChart();
    },
    methods: {
      renderChart() {
        const options = {
          series: [{
            name: "Sales",
            data: [{
                x: 'Jan',
                y: 85000,
            }, {
                x: 'Feb',
                y: 70000,
            }, {
                x: 'Mar',
                y: 40000,
            }, {
                x: 'Apr',
                y: 50000,
            }, {
                x: 'May',
                y: 60000,
            }, {
                x: 'Jun',
                y: 50000,
            }, {
                x: 'Jul',
                y: 40000,
            }, {
                x: 'Aug',
                y: 50000,
            }, {
                x: 'Sep',
                y: 40000,
            }, {
                x: 'Oct',
                y: 60000,
            }, {
                x: 'Nov',
                y: 30000,
            }, {
                x: 'Dec',
                y: 50000,
            }]
          }],
          chart: {
              type: 'bar',
              height: 264,
              toolbar: {
                  show: false
              }
          },
          plotOptions: {
              bar: {
                  horizontal: false,
                  borderRadius: 8,
                  columnWidth: 10,
                  borderRadiusApplication: 'end', // 'around', 'end'
                  borderRadiusWhenStacked: 'last', // 'all', 'last'
                  columnWidth: '23%',
                  endingShape: 'rounded',
              }
          },
          dataLabels: {
              enabled: false
          },
          fill: {
              type: 'gradient',
              colors: ['#487FFF'], // Set the starting color (top color) here
              gradient: {
                  shade: 'light', // Gradient shading type
                  type: 'vertical',  // Gradient direction (vertical)
                  shadeIntensity: 0.5, // Intensity of the gradient shading
                  gradientToColors: ['#487FFF'], // Bottom gradient color (with transparency)
                  inverseColors: false, // Do not invert colors
                  opacityFrom: 1, // Starting opacity
                  opacityTo: 1,  // Ending opacity
                  stops: [0, 100],
              },
          },
          grid: {
              show: true,
              borderColor: '#D1D5DB',
              strokeDashArray: 4, // Use a number for dashed style
              position: 'back',
          },
          xaxis: {
              type: 'category',
              categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
          },
          yaxis: {
              labels: {
                  formatter: function (value) {
                      return (value / 1000).toFixed(0) + 'k';
                  }
              }
          },
          tooltip: {
              y: {
                  formatter: function (value) {
                      return value / 1000 + 'k';
                  }
              }
          }
        };
  
        const chart = new ApexCharts(document.querySelector("#columnGroupBarChart"), options);
        chart.render();
      }
    }
  }
  </script>
  