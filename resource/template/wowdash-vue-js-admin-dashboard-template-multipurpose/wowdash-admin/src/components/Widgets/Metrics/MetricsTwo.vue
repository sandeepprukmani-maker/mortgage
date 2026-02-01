<template>
    <div class="mt-24">
      <div class="row gy-4">
        <div class="col-xxl-3 col-sm-6" v-for="(card, index) in cards" :key="index">
          <div :class="`card p-3 shadow-none radius-8 border h-100 ${card.bgClass}`">
            <div class="card-body p-0">
              <div class="d-flex flex-wrap align-items-center justify-content-between gap-1 mb-8">
                <div class="d-flex align-items-center gap-2">
                  <span :class="`mb-0 w-48-px h-48-px ${card.iconBgClass} flex-shrink-0 text-white d-flex justify-content-center align-items-center rounded-circle h6`">
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
                <span :class="`bg-${card.increaseClass} px-1 rounded-2 fw-medium text-${card.increaseColor} text-sm`">
                  {{ card.increaseValue }}
                </span> 
                this week
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from "apexcharts";
  import VueApexCharts from 'vue3-apexcharts'; // For integration of ApexCharts in Vue
  
  export default {
    components: {
      apexchart: VueApexCharts
    },
    data() {
      return {
        cards: [
          {
            title: 'New Users',
            value: '15,000',
            bgClass: 'bg-gradient-end-1',
            iconBgClass: 'bg-primary-600',
            icon: 'mingcute:user-follow-fill',
            chartId: 'new-user-chart',
            increaseClass: 'success-focus',
            increaseColor: 'success-main',
            increaseValue: '+200',
          },
          {
            title: 'Active Users',
            value: '8,000',
            bgClass: 'bg-gradient-end-2',
            iconBgClass: 'bg-success-main',
            icon: 'mingcute:user-follow-fill',
            chartId: 'active-user-chart',
            increaseClass: 'success-focus',
            increaseColor: 'success-main',
            increaseValue: '+200',
          },
          {
            title: 'Total Sales',
            value: '$5,00,000',
            bgClass: 'bg-gradient-end-3',
            iconBgClass: 'bg-yellow',
            icon: 'iconamoon:discount-fill',
            chartId: 'total-sales-chart',
            increaseClass: 'danger-focus',
            increaseColor: 'danger-main',
            increaseValue: '-$10k',
          },
          {
            title: 'Conversion',
            value: '25%',
            bgClass: 'bg-gradient-end-3',
            iconBgClass: 'bg-purple',
            icon: 'mdi:message-text',
            chartId: 'conversion-user-chart',
            increaseClass: 'success-focus',
            increaseColor: 'success-main',
            increaseValue: '+5%',
          }
        ]
      };
    },
    mounted() {
      this.createWidgetChart('new-user-chart', '#487fff');
      this.createWidgetChart('active-user-chart', '#45b369');
      this.createWidgetChart('total-sales-chart', '#f4941e');
      this.createWidgetChart('conversion-user-chart', '#8252e9');
    },
    methods: {
      createWidgetChart(chartId, chartColor) {
        let currentYear = new Date().getFullYear();
  
        var options = {
          series: [
            {
              name: 'series1',
              data: [35, 45, 38, 41, 36, 43, 37, 55, 40],
            },
          ],
          chart: {
            type: 'area',
            width: 100,
            height: 42,
            sparkline: {
              enabled: true // Remove whitespace
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
            curve: 'smooth',
            width: 2,
            colors: [chartColor],
            lineCap: 'round'
          },
          grid: {
            show: true,
            borderColor: 'transparent',
            strokeDashArray: 0,
            position: 'back',
            xaxis: {
              lines: {
                show: false
              }
            },   
            yaxis: {
              lines: {
                show: false
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
              top: -3,
              right: 0,
              bottom: 0,
              left: 0
            },
          },
          fill: {
            type: 'gradient',
            colors: [chartColor], // Set the starting color (top color) here
            gradient: {
              shade: 'light', // Gradient shading type
              type: 'vertical',  // Gradient direction (vertical)
              shadeIntensity: 0.5, // Intensity of the gradient shading
              gradientToColors: [`${chartColor}00`], // Bottom gradient color (with transparency)
              inverseColors: false, // Do not invert colors
              opacityFrom: .75, // Starting opacity
              opacityTo: 0.3,  // Ending opacity
              stops: [0, 100],
            },
          },
          markers: {
            colors: [chartColor],
            strokeWidth: 2,
            size: 0,
            hover: {
              size: 8
            }
          },
          xaxis: {
            labels: {
              show: false
            },
            categories: [`Jan ${currentYear}`, `Feb ${currentYear}`, `Mar ${currentYear}`, `Apr ${currentYear}`, `May ${currentYear}`, `Jun ${currentYear}`, `Jul ${currentYear}`, `Aug ${currentYear}`, `Sep ${currentYear}`, `Oct ${currentYear}`, `Nov ${currentYear}`, `Dec ${currentYear}`],
            tooltip: {
              enabled: false,
            },
          },
          yaxis: {
            labels: {
              show: false
            }
          },
          tooltip: {
            x: {
              format: 'dd/MM/yy HH:mm'
            },
          },
        };
  
        var chart = new ApexCharts(document.querySelector(`#${chartId}`), options);
        chart.render();
      }
    }
  };
  </script>