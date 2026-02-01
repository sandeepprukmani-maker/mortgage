<template>
    <div class="col-xxl-4">
      <div class="card h-100 radius-8 border-0">
        <div class="card-body p-24">
          <h6 class="mb-2 fw-bold text-lg">Statistic</h6>
          <div class="mt-24">
            <div class="d-flex align-items-center gap-1 justify-content-between mb-44">
              <div>
                <span class="text-secondary-light fw-normal mb-12 text-xl">Daily Conversions</span>
                <h5 class="fw-semibold mb-0">%60</h5>
              </div>
              <div class="position-relative">
                <div id="semiCircleGauge"></div>
                <span class="w-36-px h-36-px rounded-circle bg-neutral-100 d-flex justify-content-center align-items-center position-absolute start-50 translate-middle top-100">
                  <iconify-icon icon="mdi:emoji" class="text-primary-600 text-md mb-0"></iconify-icon>
                </span>
              </div>
            </div>
  
            <div class="d-flex align-items-center gap-1 justify-content-between mb-44">
              <div>
                <span class="text-secondary-light fw-normal mb-12 text-xl">Visits By Day</span>
                <h5 class="fw-semibold mb-0">20k</h5>
              </div>
              <div id="areaChart"></div>
            </div>
  
            <div class="d-flex align-items-center gap-1 justify-content-between">
              <div>
                <span class="text-secondary-light fw-normal mb-12 text-xl">Today Income</span>
                <h5 class="fw-semibold mb-0">$5.5k</h5>
              </div>
              <div id="dailyIconBarChart"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts';
  import VueApexCharts from 'vue3-apexcharts'; 
  
  export default {
    name: 'DashboardStats',
    components: {
      apexchart: VueApexCharts,
    },
    mounted() {
      this.renderCharts();
    },
    methods: {
      renderCharts() {
        // ================================ Semi Circle Gauge (Daily Conversion) chart Start ================================ 
        var options = {
          series: [75],
          chart: {
            width: 200,
            type: 'radialBar',
            sparkline: {
              enabled: true, // Remove whitespace
            },
            toolbar: {
              show: false,
            },
          },
          plotOptions: {
            radialBar: {
              offsetY: -24,
              offsetX: -14,
              startAngle: -90,
              endAngle: 90,
              track: {
                background: "#E3E6E9",
                dropShadow: {
                  enabled: false,
                  top: 2,
                  left: 0,
                  color: '#999',
                  opacity: 1,
                  blur: 2,
                },
              },
              dataLabels: {
                show: false,
                name: {
                  show: false,
                },
                value: {
                  offsetY: -2,
                  fontSize: '22px',
                },
              },
            },
          },
          fill: {
            type: 'gradient',
            colors: ['#9DBAFF'],
            gradient: {
              shade: 'dark',
              type: 'horizontal',
              shadeIntensity: 0.5,
              gradientToColors: ['#487FFF'],
              inverseColors: true,
              opacityFrom: 1,
              opacityTo: 1,
              stops: [0, 100],
            },
          },
          stroke: {
            lineCap: 'round',
          },
          labels: ['Percent'],
        };
  
        var chart = new ApexCharts(document.querySelector("#semiCircleGauge"), options);
        chart.render();
        // ================================ Semi Circle Gauge (Daily Conversion) chart End ================================ 
  
        // ================================ Area chart Start ================================ 
        this.createChart('areaChart', '#FF9F29');
        // ================================ Area chart End ================================ 
  
        // ================================ Bar chart (Today Income) Start ================================ 
        var barChartOptions = {
          series: [{
            name: "Sales",
            data: [
              { x: 'Mon', y: 20 },
              { x: 'Tue', y: 40 },
              { x: 'Wed', y: 20 },
              { x: 'Thur', y: 30 },
              { x: 'Fri', y: 40 },
              { x: 'Sat', y: 35 },
            ]
          }],
          chart: {
            type: 'bar',
            width: 164,
            height: 80,
            sparkline: {
              enabled: true, // Remove whitespace
            },
            toolbar: {
              show: false,
            }
          },
          plotOptions: {
            bar: {
              borderRadius: 6,
              horizontal: false,
              columnWidth: 14,
            }
          },
          dataLabels: {
            enabled: false,
          },
          states: {
            hover: {
              filter: {
                type: 'none',
              }
            }
          },
          fill: {
            type: 'gradient',
            colors: ['#E3E6E9'],
            gradient: {
              shade: 'light',
              type: 'vertical',
              shadeIntensity: 0.5,
              gradientToColors: ['#E3E6E9'],
              inverseColors: false,
              opacityFrom: 1,
              opacityTo: 1,
              stops: [0, 100],
            },
          },
          grid: {
            show: false,
            borderColor: '#D1D5DB',
            strokeDashArray: 1,
            position: 'back',
          },
          xaxis: {
            labels: {
              show: false,
            },
            type: 'category',
            categories: ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat'],
          },
          yaxis: {
            labels: {
              show: false,
              formatter: function (value) {
                return (value / 1000).toFixed(0) + 'k';
              },
            },
          },
          tooltip: {
            y: {
              formatter: function (value) {
                return value / 1000 + 'k';
              },
            },
          }
        };
  
        var barChart = new ApexCharts(document.querySelector("#dailyIconBarChart"), barChartOptions);
        barChart.render();
        // ================================ Bar chart (Today Income) End ================================
      },
      createChart(chartId, chartColor) {
        let currentYear = new Date().getFullYear();
  
        var options = {
          series: [{
            name: 'series1',
            data: [0, 10, 8, 25, 15, 26, 13, 35, 15, 39, 16, 46, 42],
          }],
          chart: {
            type: 'area',
            width: 164,
            height: 72,
            sparkline: {
              enabled: true, // Remove whitespace
            },
            toolbar: {
              show: false,
            },
            padding: {
              left: 0,
              right: 0,
              top: 0,
              bottom: 0,
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
            borderColor: 'transparent',
            strokeDashArray: 0,
            position: 'back',
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
            row: {
              colors: undefined,
              opacity: 0.5,
            },
            column: {
              colors: undefined,
              opacity: 0.5,
            },
            padding: {
              top: -3,
              right: 0,
              bottom: 0,
              left: 0,
            },
          },
          colors: [chartColor],
          fill: {
            type: 'gradient',
            colors: [chartColor],
            gradient: {
              shade: 'light',
              type: 'vertical',
              shadeIntensity: 0.5,
              gradientToColors: [`${chartColor}00`],
              inverseColors: false,
              opacityFrom: 0.8,
              opacityTo: 0.3,
              stops: [0, 100],
            },
          },
          markers: {
            colors: [chartColor],
            strokeWidth: 2,
            size: 0,
            hover: {
              size: 8,
            },
          },
          xaxis: {
            labels: {
              show: false,
            },
            categories: [`Jan ${currentYear}`, `Feb ${currentYear}`, `Mar ${currentYear}`, `Apr ${currentYear}`, `May ${currentYear}`, `Jun ${currentYear}`, `Jul ${currentYear}`, `Aug ${currentYear}`, `Sep ${currentYear}`, `Oct ${currentYear}`, `Nov ${currentYear}`, `Dec ${currentYear}`],
            tooltip: {
              enabled: false,
            },
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
        };
  
        var chart = new ApexCharts(document.querySelector(`#${chartId}`), options);
        chart.render();
      },
    },
  };
  </script>