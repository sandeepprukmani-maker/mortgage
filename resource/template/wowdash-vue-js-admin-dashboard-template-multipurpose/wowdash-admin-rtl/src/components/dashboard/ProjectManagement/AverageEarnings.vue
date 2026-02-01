<template>
    <div class="col-xxl-8">
      <div class="card h-100 radius-8 border-0">
        <div class="card-header border-bottom bg-base py-16 px-24 d-flex align-items-center justify-content-between">
          <h6 class="text-lg fw-semibold mb-0">Average Earnings</h6>
          <div>
            <select class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8">
              <option>Yearly</option>
              <option>Monthly</option>
              <option>Weekly</option>
              <option>Today</option>
            </select>
          </div>
        </div>
        <div class="card-body p-24">
          <ul class="d-flex flex-wrap align-items-center justify-content-center my-3 gap-3">
            <li class="d-flex align-items-center gap-2">
              <span class="w-12-px h-8-px rounded-pill bg-primary-600"></span>
              <span class="text-secondary-light text-sm fw-semibold">
                Income:
                <span class="text-primary-light text-xl fw-bold line-height-1">$26,201</span>
              </span>
            </li>
            <li class="d-flex align-items-center gap-2">
              <span class="w-12-px h-8-px rounded-pill bg-warning-600"></span>
              <span class="text-secondary-light text-sm fw-semibold">
                Expense:
                <span class="text-primary-light text-xl fw-bold line-height-1"> $3,120</span>
              </span>
            </li>
          </ul>
          <div id="averageEarningChart" class="apexcharts-tooltip-style-1"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts'
  
  export default {
    name: 'AverageEarnings',
    mounted() {
      this.createChartTwo('averageEarningChart', '#487FFF', '#FF9F29');
    },
    methods: {
      createChartTwo(chartId, color1, color2) {
        var options = {
          series: [
            {
              name: 'Income',
              data: [48, 35, 55, 32, 48, 30, 55, 50, 57]
            },
            {
              name: 'Expense',
              data: [12, 20, 15, 26, 22, 60, 40, 48, 25]
            }
          ],
          legend: {
            show: false
          },
          chart: {
            type: 'line',
            width: '100%',
            height: 270,
            toolbar: { show: false },
            padding: { left: 0, right: 0, top: 0, bottom: 0 }
          },
          dataLabels: { enabled: false },
          stroke: {
            curve: 'smooth',
            width: 3,
            colors: [color1, color2],
            lineCap: 'round'
          },
          grid: {
            show: true,
            borderColor: '#D1D5DB',
            strokeDashArray: 1,
            position: 'back',
            xaxis: { lines: { show: false } },
            yaxis: { lines: { show: true } },
            row: { colors: undefined, opacity: 0.5 },
            column: { colors: undefined, opacity: 0.5 },
            padding: { top: -20, right: 0, bottom: -10, left: 0 }
          },
          colors: [color1, color2],
          markers: {
            colors: [color1, color2],
            strokeWidth: 3,
            size: 0,
            hover: { size: 10 }
          },
          xaxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            tooltip: { enabled: false },
            labels: {
              formatter: function (value) {
                return value;
              },
              style: { fontSize: '14px' }
            }
          },
          yaxis: {
            min:0,
            max:70,
            labels: {
              formatter: function (value) {
                return '$' + value + 'k';
              },
              style: { fontSize: '14px' }
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
  }
  </script>
  