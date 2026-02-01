<template>
    <div class="col-xxl-12 col-md-6">
      <div class="card h-100">
        <div class="card-header border-bottom d-flex align-items-center flex-wrap gap-2 justify-content-between">
          <h6 class="fw-bold text-lg mb-0">ETH Price</h6>
          <select class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8 rounded-pill">
            <option>November</option>
            <option>December</option>
            <option>January</option>
            <option>February</option>
            <option>March</option>
            <option>April</option>
            <option>May</option>
            <option>June</option>
            <option>July</option>
            <option>August</option>
            <option>September</option>
          </select>
        </div>
        <div class="card-body">
          <div id="enrollmentChart" class="apexcharts-tooltip-style-1 yaxies-more"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts'
  
  export default {
    name: 'EthPriceChart',
    mounted() {
      this.createChartTwo('enrollmentChart', '#487FFF', '#487FFF')
    },
    methods: {
      createChartTwo(chartId, color1, color2) {
        const options = {
          series: [{
            name: 'series2',
            data: [20000, 45000, 30000, 50000, 32000, 40000, 30000, 42000, 28000, 34000, 38000, 26000]
          }],
          legend: { show: false },
          chart: {
            type: 'area',
            width: '100%',
            height: 240,
            toolbar: { show: false },
            padding: { left: 0, right: 0, top: 0, bottom: 0 }
          },
          dataLabels: { enabled: false },
          stroke: {
            curve: 'straight',
            width: 3,
            colors: [color1],
            lineCap: 'round'
          },
          grid: {
            show: true,
            borderColor: '#D1D5DB',
            strokeDashArray: 1,
            position: 'back',
            xaxis: { lines: { show: false }},
            yaxis: { lines: { show: true }},
            row: { opacity: 0.5 },
            column: { opacity: 0.5 },
            padding: { top: -20, right: 0, bottom: 0, left: 0 }
          },
          fill: {
            type: 'gradient',
            colors: [color1],
            gradient: {
              shade: 'light',
              type: 'vertical',
              shadeIntensity: 0.5,
              gradientToColors: [undefined, `${color2}00`],
              inverseColors: false,
              opacityFrom: [0.4, 0.4],
              opacityTo: [0.1, 0.1],
              stops: [0, 100],
            }
          },
          markers: {
            colors: [color1],
            strokeWidth: 3,
            size: 0,
            hover: { size: 10 }
          },
          xaxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            tooltip: { enabled: false },
            labels: {
              formatter: value => value,
              style: { fontSize: "12px" }
            }
          },
          yaxis: {
            min: 16000,
            max: 56000,
            tickAmount: 5,
            labels: {
              style: { fontSize: "12px" }
            }
          },
          tooltip: {
            x: { format: 'dd/MM/yy HH:mm' }
          }
        }
  
        const chart = new ApexCharts(document.querySelector(`#${chartId}`), options)
        chart.render()
      }
    }
  }
  </script>
  