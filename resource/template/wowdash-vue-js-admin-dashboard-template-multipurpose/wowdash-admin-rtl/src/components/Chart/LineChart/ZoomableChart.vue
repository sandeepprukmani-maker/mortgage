<template>
    <div class="col-md-6">
      <div class="card h-100 p-0">
        <div class="card-header border-bottom bg-base py-16 px-24">
          <h6 class="text-lg fw-semibold mb-0">Zoomable Chart</h6>
        </div>
        <div class="card-body p-24">
          <div id="zoomAbleLineChart"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts'
  
  export default {
    name: 'ZoomableChart',
    mounted() {
      this.createChartTwo('zoomAbleLineChart', '#487fff');
    },
    methods: {
      createChartTwo(chartId, chartColor) {
        const options = {
          series: [
            {
              name: 'This Day',
              data: [12, 18, 12, 48, 18, 30, 18, 15, 88, 40, 65, 24, 48],
            },
          ],
          chart: {
            type: 'area',
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
          dataLabels: {
            enabled: false
          },
          stroke: {
            curve: 'straight',
            width: 4,
            colors: [chartColor],
            lineCap: 'round'
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
          fill: {
            type: 'gradient',
            colors: [chartColor],
            gradient: {
              shade: 'light',
              type: 'vertical',
              shadeIntensity: 0.5,
              gradientToColors: [`${chartColor}00`],
              inverseColors: false,
              opacityFrom: 0.6,
              opacityTo: 0.3,
              stops: [0, 100],
            }
          },
          markers: {
            colors: [chartColor],
            strokeWidth: 3,
            size: 0,
            hover: {
              size: 10
            }
          },
          xaxis: {
            labels: {
              show: true,
              formatter: function (value) {
                return value;
              },
              style: {
                fontSize: "14px"
              }
            },
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            tooltip: {
              enabled: false
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
          }
        };
  
        const chart = new ApexCharts(document.querySelector(`#${chartId}`), options);
        chart.render();
      }
    }
  };
  </script>
  