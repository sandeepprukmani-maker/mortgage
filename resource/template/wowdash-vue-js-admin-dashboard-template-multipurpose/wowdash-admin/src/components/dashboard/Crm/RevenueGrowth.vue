<template>
    <div class="col-xxl-4">
      <div class="card h-100 radius-8 border">
        <div class="card-body p-24">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
            <div>
              <h6 class="mb-2 fw-bold text-lg">Revenue Growth</h6>
              <span class="text-sm fw-medium text-secondary-light">Weekly Report</span>
            </div>
            <div class="text-end">
              <h6 class="mb-2 fw-bold text-lg">$50,000.00</h6>
              <span class="bg-success-focus ps-12 pe-12 pt-2 pb-2 rounded-2 fw-medium text-success-main text-sm">
                $10k
              </span>
            </div>
          </div>
          <div id="revenue-chart" class="mt-28"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { onMounted } from 'vue'
  import ApexCharts from 'apexcharts'
  
  // Chart colors
  const chartId = 'revenue-chart'
  const chartColor = '#487fff'
  
  const createChart = () => {
    const options = {
      series: [
        {
          name: 'This Day',
          data: [4, 18, 13, 40, 30, 50, 30, 60, 40, 75, 45, 90],
        },
      ],
      chart: {
        type: 'area',
        width: '100%',
        height: 162,
        sparkline: {
          enabled: false,
        },
        toolbar: {
          show: false,
        },
      },
      dataLabels: {
        enabled: false,
      },
      stroke: {
        curve: 'smooth',
        width: 2,
        colors: [chartColor],
        lineCap: 'round',
      },
      grid: {
        show: true,
        borderColor: 'red',
        strokeDashArray: 0,
        xaxis: {
          lines: {
            show: false,
          },
        },
        yaxis: {
          lines: {
            show: false,
          },
        },
        padding: {
          top: -30,
          right: 0,
          bottom: -10,
          left: 0,
        },
      },
      colors: [chartColor],
      fill: {
        type: 'gradient',
        gradient: {
          shade: 'light',
          type: 'vertical',
          shadeIntensity: 0.5,
          gradientToColors: [`${chartColor}00`],
          inverseColors: false,
          opacityFrom: 0.6,
          opacityTo: 0.3,
          stops: [0, 100],
        },
      },
      markers: {
        colors: [chartColor],
        strokeWidth: 3,
        size: 0,
        hover: {
          size: 10,
        },
      },
      xaxis: {
        labels: {
          show: true,
          style: {
            fontSize: '14px',
          },
        },
        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
      },
      yaxis: {
        labels: {
          show: false,
        },
      },
      tooltip: {
        x: {
          format: 'dd/MM/yy HH:mm',
        },
      },
    }
  
    const chart = new ApexCharts(document.querySelector(`#${chartId}`), options)
    chart.render()
  }
  
  onMounted(() => {
    createChart()
  })
  </script>
  
  <style scoped>
  /* Add your scoped styles if needed */
  </style>
  