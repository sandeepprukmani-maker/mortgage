<template>
    <div class="row row-cols-xxxl-5 row-cols-lg-3 row-cols-sm-2 row-cols-1 gy-4">
      
      <!-- Bitcoin Card -->
      <div class="col">
        <div class="card shadow-none border bg-gradient-end-3">
          <div class="card-body p-20">
            <div class="d-flex flex-wrap align-items-center justify-content-between gap-3">
              <img src="@/assets/images/currency/crypto-img1.png" alt="" class="w-40-px h-40-px rounded-circle flex-shrink-0">
              <div class="flex-grow-1">
                <h6 class="text-xl mb-1">Bitcoin</h6>
                <p class="fw-medium text-secondary-light mb-0">BTC</p>
              </div>
            </div>
            <div class="mt-3 d-flex flex-wrap justify-content-between align-items-center gap-1">
              <div>
                <h6 class="mb-8">$45,138</h6>
                <span class="text-success-main text-md">+ 27%</span>
              </div>
              <div id="bitcoinAreaChart" class="remove-tooltip-title rounded-tooltip-value"></div>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Ethereum Card -->
      <div class="col">
        <div class="card shadow-none border bg-gradient-end-1">
          <div class="card-body p-20">
            <div class="d-flex flex-wrap align-items-center justify-content-between gap-3">
              <img src="@/assets/images/currency/crypto-img2.png" alt="" class="w-40-px h-40-px rounded-circle flex-shrink-0">
              <div class="flex-grow-1">
                <h6 class="text-xl mb-1">Ethereum</h6>
                <p class="fw-medium text-secondary-light mb-0">ETH</p>
              </div>
            </div>
            <div class="mt-3 d-flex flex-wrap justify-content-between align-items-center gap-1">
              <div>
                <h6 class="mb-8">$45,138</h6>
                <span class="text-danger-main text-md">- 27%</span>
              </div>
              <div id="ethereumAreaChart" class="remove-tooltip-title rounded-tooltip-value"></div>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Solana Card -->
      <div class="col">
        <div class="card shadow-none border bg-gradient-end-5">
          <div class="card-body p-20">
            <div class="d-flex flex-wrap align-items-center justify-content-between gap-3">
              <img src="@/assets/images/currency/crypto-img3.png" alt="" class="w-40-px h-40-px rounded-circle flex-shrink-0">
              <div class="flex-grow-1">
                <h6 class="text-xl mb-1">Solana</h6>
                <p class="fw-medium text-secondary-light mb-0">SOL</p>
              </div>
            </div>
            <div class="mt-3 d-flex flex-wrap justify-content-between align-items-center gap-1">
              <div>
                <h6 class="mb-8">$45,138</h6>
                <span class="text-success-main text-md">+ 27%</span>
              </div>
              <div id="solanaAreaChart" class="remove-tooltip-title rounded-tooltip-value"></div>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Litecoin Card -->
      <div class="col">
        <div class="card shadow-none border bg-gradient-end-6">
          <div class="card-body p-20">
            <div class="d-flex flex-wrap align-items-center justify-content-between gap-3">
              <img src="@/assets/images/currency/crypto-img4.png" alt="" class="w-40-px h-40-px rounded-circle flex-shrink-0">
              <div class="flex-grow-1">
                <h6 class="text-xl mb-1">Litecoin</h6>
                <p class="fw-medium text-secondary-light mb-0">LTE</p>
              </div>
            </div>
            <div class="mt-3 d-flex flex-wrap justify-content-between align-items-center gap-1">
              <div>
                <h6 class="mb-8">$45,138</h6>
                <span class="text-success-main text-md">+ 27%</span>
              </div>
              <div id="litecoinAreaChart" class="remove-tooltip-title rounded-tooltip-value"></div>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Dogecoin Card -->
      <div class="col">
        <div class="card shadow-none border bg-gradient-end-3">
          <div class="card-body p-20">
            <div class="d-flex flex-wrap align-items-center justify-content-between gap-3">
              <img src="@/assets/images/currency/crypto-img5.png" alt="" class="w-40-px h-40-px rounded-circle flex-shrink-0">
              <div class="flex-grow-1">
                <h6 class="text-xl mb-1">Dogecoin</h6>
                <p class="fw-medium text-secondary-light mb-0">DOGE</p>
              </div>
            </div>
            <div class="mt-3 d-flex flex-wrap justify-content-between align-items-center gap-1">
              <div>
                <h6 class="mb-8">$45,138</h6>
                <span class="text-success-main text-md">+ 27%</span>
              </div>
              <div id="dogecoinAreaChart" class="remove-tooltip-title rounded-tooltip-value"></div>
            </div>
          </div>
        </div>
      </div>
  
    </div>
  </template>
  
  <script>
  import ApexCharts from "apexcharts";
  import { onMounted } from "vue";
  
  export default {
    name: "CryptoCard",
    setup() {
      const createChart = (chartId, chartColor) => {
        const currentYear = new Date().getFullYear();
  
        const options = {
          series: [
            {
              name: 'series1',
              data: [31, 24, 30, 25, 32, 28, 40, 32, 42, 38, 40, 32, 38, 35, 45],
            },
          ],
          chart: {
            type: 'area',
            width: 130,
            height: 50,
            sparkline: {
              enabled: true
            },
            toolbar: {
              show: false
            },
            padding: {
              left: 0,
              right: 0,
              top: 0,
              bottom: 0
            },
            events: {
              mounted: function (chartContext, config) {
                document.querySelectorAll(`#${chartId} .apexcharts-marker`).forEach(marker => {
                  marker.style.filter = 'blur(2px)';
                });
              },
              updated: function (chartContext, config) {
                document.querySelectorAll(`#${chartId} .apexcharts-marker`).forEach(marker => {
                  marker.style.filter = 'blur(3px)';
                });
              }
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
            padding: {
              top: -3,
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
              opacityFrom: .7,
              opacityTo: 0.3,
              stops: [0, 100],
            }
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
            }
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
  
        const chart = new ApexCharts(document.querySelector(`#${chartId}`), options);
        chart.render();
      };
  
      onMounted(() => {
        createChart('bitcoinAreaChart', '#F98C08');
        createChart('ethereumAreaChart', '#5F80FF');
        createChart('solanaAreaChart', '#C817F8');
        createChart('litecoinAreaChart', '#2171EA');
        createChart('dogecoinAreaChart', '#C2A633');
      });
  
      return {};
    }
  };
  </script>