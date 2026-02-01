<template>
    <div class="col-lg-8">
      <div class="shadow-7 p-0 radius-12 bg-base h-100 overflow-hidden">
        <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between py-12 px-20 border-bottom border-neutral-200">
          <h6 class="mb-0 fw-bold text-lg">Pending Vs Solved Tickets</h6>
          <div>
            <select class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8">
              <option>Yearly</option>
              <option>Monthly</option>
              <option>Weekly</option>
              <option>Today</option>
            </select>
          </div>
        </div>
        <div class="card-body p-20">
          <ul class="d-flex flex-wrap align-items-center justify-content-center my-3 gap-3">
            <li class="d-flex align-items-center gap-2">
              <span class="w-12-px h-8-px rounded-pill bg-warning-600"></span>
              <div class="d-flex align-items-center gap-1">
                <span class="text-secondary-light text-sm fw-semibold">Pending: </span>
                <h6 class="text-primary-light fw-bold">505</h6>
              </div>
            </li>
            <li class="d-flex align-items-center gap-2">
              <span class="w-12-px h-8-px rounded-pill bg-success-600"></span>
              <div class="d-flex align-items-center gap-1">
                <span class="text-secondary-light text-sm fw-semibold">Solved:</span>
                <h6 class="text-primary-light fw-bold">700</h6>
              </div>
            </li>
          </ul>
          <div id="pendingSolvedTicket" class="apexcharts-tooltip-style-1"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts';
  
  export default {
    name: 'PendingSolvedTicketsCard',
    mounted() {
      this.createChartOne('pendingSolvedTicket', '#45B369', '#FF9F29');
    },
    methods: {
      createChartOne(chartId, color1, color2) {
        const options = {
          series: [
            {
              name: 'Pending',
              data: [480, 350, 550, 320, 480, 300, 550, 500, 570]
            },
            {
              name: 'Solved',
              data: [120, 200, 150, 260, 220, 600, 400, 480, 250]
            }
          ],
          legend: {
            show: false
          },
          chart: {
            type: 'area',
            width: '100%',
            height: 200,
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
            curve: 'smooth',
            width: 3,
            colors: [color1, color2], // Use two colors for the lines
            lineCap: 'round'
          },
          grid: {
            show: true,
            borderColor: '#D1D5DB',
            strokeDashArray: 1,
            position: 'back',
            xaxis: {
              lines: {
                show: false
              }
            },
            yaxis: {
              min:0,
              max:700,
              tickAmount:6,
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
              top: -20,
              right: 0,
              bottom: -10,
              left: 0
            }
          },
          colors: [color1, color2], // Set color for series
          fill: {
            type: 'gradient',
            colors: [color1, color2], // Use two colors for the gradient
            gradient: {
              shade: 'light',
              type: 'vertical',
              shadeIntensity: 0.5,
              gradientToColors: [undefined, `${color2}00`], // Apply transparency to both colors
              inverseColors: false,
              opacityFrom: [0.4, 0.6], // Starting opacity for both colors
              opacityTo: [0.3, 0.3], // Ending opacity for both colors
              stops: [0, 100]
            }
          },
          markers: {
            colors: [color1, color2], // Use two colors for the markers
            strokeWidth: 3,
            size: 0,
            hover: {
              size: 10
            }
          },
          xaxis: {
            labels: {
              show: false
            },
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            tooltip: {
              enabled: false
            },
            labels: {
              formatter: function (value) {
                return value;
              },
              style: {
                fontSize: '14px'
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
  
  <style scoped>
  /* Add your styles here if any */
  </style>
  