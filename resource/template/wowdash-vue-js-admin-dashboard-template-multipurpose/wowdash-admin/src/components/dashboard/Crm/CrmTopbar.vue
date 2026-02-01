<template>
    <div class="col-xxl-8">
      <div class="row gy-4">
        <div
          v-for="(card, index) in cards"
          :key="index"
          :class="`col-xxl-4 col-sm-6`"
        >
          <div :class="`card p-3 shadow-2 radius-8 border input-form-light h-100 ${card.bgGradient}`">
            <div class="card-body p-0">
              <div class="d-flex flex-wrap align-items-center justify-content-between gap-1 mb-8">
                <div class="d-flex align-items-center gap-2">
                  <span :class="`mb-0 w-48-px h-48-px ${card.bgColor} text-white flex-shrink-0 d-flex justify-content-center align-items-center rounded-circle h6`">
                    <iconify-icon :icon="card.icon" class="icon"></iconify-icon>
                  </span>
                  <div>
                    <span class="mb-2 fw-medium text-secondary-light text-sm">{{ card.title }}</span>
                    <h6 class="fw-semibold">{{ card.value }}</h6>
                  </div>
                </div>
                <div :id="card.chartId" class="remove-tooltip-title rounded-tooltip-value"></div>
              </div>
              <p class="text-sm mb-0">
                Increase by
                <span :class="`px-1 rounded-2 fw-medium text-sm ${card.increaseClass}`">
                  {{ card.increase }}
                </span>
                this week
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { onMounted } from 'vue'
  import ApexCharts from 'apexcharts'
  
  const cards = [
    {
      title: 'New Users',
      value: '15,000',
      increase: '+200',
      increaseClass: 'bg-success-focus text-success-main',
      chartId: 'new-user-chart',
      chartColor: '#487fff',
      bgGradient: 'bg-gradient-end-1',
      bgColor: 'bg-primary-600',
      icon: 'mingcute:user-follow-fill'
    },
    {
      title: 'Active Users',
      value: '8,000',
      increase: '+200',
      increaseClass: 'bg-success-focus text-success-main',
      chartId: 'active-user-chart',
      chartColor: '#45b369',
      bgGradient: 'bg-gradient-end-2',
      bgColor: 'bg-success-main',
      icon: 'mingcute:user-follow-fill'
    },
    {
      title: 'Total Sales',
      value: '$5,00,000',
      increase: '-$10k',
      increaseClass: 'bg-danger-focus text-danger-main',
      chartId: 'total-sales-chart',
      chartColor: '#f4941e',
      bgGradient: 'bg-gradient-end-3',
      bgColor: 'bg-yellow',
      icon: 'iconamoon:discount-fill'
    },
    {
      title: 'Conversion',
      value: '25%',
      increase: '+5%',
      increaseClass: 'bg-success-focus text-success-main',
      chartId: 'conversion-user-chart',
      chartColor: '#8252e9',
      bgGradient: 'bg-gradient-end-4',
      bgColor: 'bg-purple',
      icon: 'mdi:message-text'
    },
    {
      title: 'Leads',
      value: '250',
      increase: '+20',
      increaseClass: 'bg-success-focus text-success-main',
      chartId: 'leads-chart',
      chartColor: '#de3ace',
      bgGradient: 'bg-gradient-end-5',
      bgColor: 'bg-pink',
      icon: 'mdi:leads'
    },
    {
      title: 'Total Profit',
      value: '$3,00,700',
      increase: '+$15k',
      increaseClass: 'bg-success-focus text-success-main',
      chartId: 'total-profit-chart',
      chartColor: '#00b8f2',
      bgGradient: 'bg-gradient-end-6',
      bgColor: 'bg-cyan',
      icon: 'streamline:bag-dollar-solid'
    }
  ]
  
  function createChart(chartId, chartColor) {
    let currentYear = new Date().getFullYear()
  
    const options = {
      series: [
        {
          name: 'series1',
          data: [35, 45, 38, 41, 36, 43, 37, 55, 40]
        }
      ],
      chart: {
        type: 'area',
        width: 80,
        height: 42,
        sparkline: { enabled: true },
        toolbar: { show: false }
      },
      dataLabels: { enabled: false },
      stroke: {
        curve: 'smooth',
        width: 2,
        colors: [chartColor],
        lineCap: 'round'
      },
      grid: {
        show: true,
        borderColor: 'transparent',
        xaxis: { lines: { show: false } },
        yaxis: { lines: { show: false } },
        padding: { top: -3, right: 0, bottom: 0, left: 0 }
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
          opacityFrom: 0.75,
          opacityTo: 0.3,
          stops: [0, 100]
        }
      },
      markers: {
        colors: [chartColor],
        strokeWidth: 2,
        size: 0,
        hover: { size: 8 }
      },
      xaxis: {
        labels: { show: false },
        categories: [
          `Jan ${currentYear}`, `Feb ${currentYear}`, `Mar ${currentYear}`, `Apr ${currentYear}`,
          `May ${currentYear}`, `Jun ${currentYear}`, `Jul ${currentYear}`, `Aug ${currentYear}`,
          `Sep ${currentYear}`, `Oct ${currentYear}`, `Nov ${currentYear}`, `Dec ${currentYear}`
        ],
        tooltip: { enabled: false }
      },
      yaxis: {
        labels: { show: false }
      },
      tooltip: {
        x: { format: 'dd/MM/yy HH:mm' }
      }
    }
  
    const chart = new ApexCharts(document.querySelector(`#${chartId}`), options)
    chart.render()
  }
  
  onMounted(() => {
    cards.forEach(card => {
      createChart(card.chartId, card.chartColor)
    })
  })
  </script>
  
  <style scoped>
  /* Your additional custom styles if needed */
  </style>
  