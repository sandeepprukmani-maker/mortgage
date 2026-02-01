<template>
    <div class="col-xxl-9 col-lg-8">
      <div class="card h-100 p-0 radius-12">
        <div class="card-body px-24 py-32">
          <div class="d-flex align-items-center justify-content-between mb-24">
            <div class="d-flex align-items-center">
              <img
                src="@/assets/images/crypto/bitcoin.png"
                alt=""
                class="w-72-px h-72-px rounded-circle flex-shrink-0 me-12 overflow-hidden"
              />
              <div class="flex-grow-1 d-flex flex-column">
                <h4 class="mb-4">Bitcoin <span class="text-md text-neutral-400 fw-semibold">BTC</span></h4>
                <span class="text-md mb-0 fw-medium text-neutral-500 d-block">Currency in USD. Market Open</span>
              </div>
            </div>
            <div class="d-flex align-items-center gap-24">
              <div class="d-flex flex-column align-items-end">
                <div class="d-flex align-items-center gap-8 mb-4">
                  <h6 class="mb-0">$0.32533</h6>
                  <span
                    class="text-sm fw-semibold rounded-pill bg-success-focus text-success-main border br-success px-8 py-4 line-height-1 d-flex align-items-center gap-1"
                  >
                    <iconify-icon icon="bxs:up-arrow" class="text-xs"></iconify-icon> 10%
                  </span>
                </div>
                <div class="">
                  <span class="fw-semibold text-secondary-light text-sm">+0,021301</span>
                  <span class="fw-semibold text-success-600 text-sm">(+6.42%)</span>
                </div>
              </div>
              <button
                type="button"
                class="star-btn w-48-px h-48-px d-flex justify-content-center align-items-center border radius-8 text-2xl text-neutral-400 text-hover-primary-600 line-height-1"
                @click="toggleStar"
              >
                <i :class="starIcon"></i>
              </button>
            </div>
          </div>
  
          <h6 class="mb-16">About</h6>
          <p class="text-secondary-light">
            IoT Chain (ITC) is a cryptocurrency and operates on the Ethereum platform. IoT Chain has a current
            supply of 99,999,999 with 87,214,657.4756 in circulation. The last known price of IoT Chain is 0.01318397 USD
            and is up 0.00 over the last 24 hours. It is currently trading on 5 active market(s) with $0.00 traded over
            the last 24 hours. More information can be found at https://iotchain.io/.
          </p>
  
          <div class="my-24">
            <div class="d-flex flex-wrap align-items-center justify-content-between">
              <h6 class="text-lg mb-0">Bitcoin Chain Price</h6>
              <select class="form-select bg-base form-select-sm w-auto radius-8" v-model="selectedTimeframe">
                <option>Yearly</option>
                <option>Monthly</option>
                <option>Weekly</option>
                <option>Today</option>
              </select>
            </div>
  
            <div>
              <div id="timeSeriesChart" class="apexcharts-tooltip-style-1"></div>
            </div>
          </div>
  
          <!-- Table Start -->
          <div class="border radius-12 p-24">
            <h6 class="text-md mb-16">Market Stats</h6>
            <div class="table-responsive scroll-sm">
              <table class="table bordered-table rounded-table sm-table mb-0">
                <thead>
                  <tr>
                    <th scope="col">Market Cap</th>
                    <th scope="col">Volume (24H)</th>
                    <th scope="col">Circulating Supply</th>
                    <th scope="col">Max Supply</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>
                      <h6 class="text-md mb-4">$1.15M</h6>
                      <span class="text-neutral-500 text-sm">39% of crypto market</span>
                    </td>
                    <td>
                      <h6 class="text-md mb-4">$146.36k</h6>
                      <span class="bg-success-focus text-success-600 px-16 py-6 rounded-pill fw-semibold text-xs">
                        <i class="ri-arrow-up-s-fill"></i> 1.37%
                      </span>
                    </td>
                    <td>
                      <h6 class="text-md mb-4">807.21M ITC</h6>
                      <span class="text-neutral-500 text-sm">91% of crypto market</span>
                    </td>
                    <td>
                      <h6 class="text-md mb-4">10B ITC</h6>
                      <div class="d-flex align-items-center gap-8 w-100-px">
                        <div class="progress w-100 bg-primary-50 rounded-pill h-4-px" role="progressbar" aria-label="Basic example" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100">
                          <div class="progress-bar bg-primary-600 rounded-pill" style="width: 50%"></div>
                        </div>
                        <span class="text-neutral-500 text-sm">8%</span>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <!-- Table End -->
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts';
  import VueApexCharts from 'vue3-apexcharts';
  
  export default {
    components: {
      apexchart: VueApexCharts
    },
    data() {
      return {
        starIcon: 'ri-star-line',  // Default state of star
        selectedTimeframe: 'Yearly',
        dates: [
          [1327359600000, 30.95],
          [1327446000000, 31.34],
          [1327532400000, 31.18],
          [1327618800000, 31.05],
          [1327878000000, 31.00],
          [1327964400000, 30.95],
          [1328050800000, 31.24],
          [1328137200000, 31.29],
          [1328223600000, 31.85],
          [1328482800000, 31.86],
          [1328569200000, 32.28],
          [1328655600000, 32.10],
          [1328742000000, 32.65],
          [1328828400000, 32.21],
          [1329087600000, 32.35],
          [1329174000000, 32.44],
          [1329260400000, 32.46],
          [1329346800000, 32.86],
          [1329433200000, 32.75],
          [1329778800000, 32.54],
          [1329865200000, 32.33],
          [1329951600000, 32.97],
          [1330038000000, 33.41],
          [1330297200000, 33.27],
          [1330383600000, 33.27],
          [1330470000000, 32.89],
          [1330556400000, 33.10],
          [1330642800000, 33.73],
        ],
      };
    },
    mounted() {
      this.renderChart();
    },
    methods: {
      toggleStar() {
        if (this.starIcon === 'ri-star-line') {
          this.starIcon = 'ri-star-fill text-primary-600';
        } else {
          this.starIcon = 'ri-star-line';
        }
      },
      renderChart() {
        const options = {
          series: [
            {
              name: 'Bitcoin',
              data: this.dates,
            },
          ],
          chart: {
            type: 'area',
            stacked: false,
            height: 350,
            zoom: {
              type: 'x',
              enabled: true,
              autoScaleYaxis: true,
            },
            toolbar: {
              show: false,
            },
          },
          stroke: {
            curve: 'straight',
            width: 2,
            color: ['#000'],
            lineCap: 'round',
          },
          dataLabels: {
            enabled: false,
          },
          markers: {
            size: 0,
          },
          grid: {
            borderColor: '#D1D5DB',
            strokeDashArray: 3,
          },
          fill: {
            type: 'gradient',
            gradient: {
              type: 'vertical',
              shadeIntensity: 1,
              gradientToColors: ['#487FFF'],
              inverseColors: false,
              opacityFrom: 0.4,
              opacityTo: 0.1,
              stops: [0, 100],
            },
          },
          yaxis: {
            tickAmount:4,
            labels: {
              formatter: function (val) {
                return (val / 1000000).toFixed(0);
              },
            },
            title: {
              text: 'Price',
            },
          },
          xaxis: {
            type: 'datetime',
          },
          tooltip: {
            shared: false,
            y: {
              formatter: function (val) {
                return (val / 1000000).toFixed(0);
              },
            },
          },
        };
  
        const chart = new ApexCharts(document.querySelector('#timeSeriesChart'), options);
        chart.render();
      },
    },
  };
  </script>