<template>
    <div class="col-xxl-3 col-xl-6">
      <div class="card h-100 radius-8 border-0 overflow-hidden">
        <div class="card-body p-24">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
            <h6 class="mb-2 fw-bold text-lg">Users Overview</h6>
            <div>
              <select 
                class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8"
                v-model="selectedTimeframe"
                @change="updateChartData">
                <option>Today</option>
                <option>Weekly</option>
                <option>Monthly</option>
                <option>Yearly</option>
              </select>
            </div>
          </div>
  
          <!-- Donut Chart -->
          <div ref="userOverviewDonutChart" class="apexcharts-tooltip-z-none"></div>
  
          <!-- Statistics -->
          <ul class="d-flex flex-wrap align-items-center justify-content-between mt-3 gap-3">
            <li class="d-flex align-items-center gap-2">
              <span class="w-12-px h-12-px radius-2 bg-primary-600"></span>
              <span class="text-secondary-light text-sm fw-normal">New:
                <span class="text-primary-light fw-semibold">{{ chartData.newUsers }}</span>
              </span>
            </li>
            <li class="d-flex align-items-center gap-2">
              <span class="w-12-px h-12-px radius-2 bg-yellow"></span>
              <span class="text-secondary-light text-sm fw-normal">Subscribed:
                <span class="text-primary-light fw-semibold">{{ chartData.subscribedUsers }}</span>
              </span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts';
  import VueApexCharts from 'vue3-apexcharts';
  
  export default {
    name: 'UserOverview',
    components: {
      VueApexCharts
    },
    data() {
      return {
        selectedTimeframe: 'Today',
        chartData: {
          activeUsers: 500,
          newUsers: 500,
          subscribedUsers: 300,
        },
        chart: null,
        options: {
          series: [500, 500, 500],
          colors: ['#FF9F29', '#487FFF', '#E4F1FF'],
          labels: ['Active', 'New', 'Total'],
          legend: {
            show: false
          },
          chart: {
            type: 'donut',
            height: 270,
            sparkline: {
              enabled: true
            },
            margin: {
              top: 0,
              right: 0,
              bottom: 0,
              left: 0
            },
            padding: {
              top: 0,
              right: 0,
              bottom: 0,
              left: 0
            }
          },
          stroke: {
            width: 0
          },
          dataLabels: {
            enabled: false
          },
          responsive: [{
            breakpoint: 480,
            options: {
              chart: {
                width: 200
              },
              legend: {
                position: 'bottom'
              }
            }
          }]
        }
      };
    },
    watch: {
      selectedTimeframe(newValue) {
        this.updateChartData(newValue);
      }
    },
    methods: {
      updateChartData() {
        // You can add your logic to update the chart data based on selectedTimeframe.
        // For now, we'll just update chart data according to selected timeframe.
        if (this.selectedTimeframe === 'Today') {
          this.chartData = { activeUsers: 500, newUsers: 500, subscribedUsers: 300 };
        } else if (this.selectedTimeframe === 'Weekly') {
          this.chartData = { activeUsers: 700, newUsers: 600, subscribedUsers: 400 };
        } else if (this.selectedTimeframe === 'Monthly') {
          this.chartData = { activeUsers: 1000, newUsers: 900, subscribedUsers: 600 };
        } else if (this.selectedTimeframe === 'Yearly') {
          this.chartData = { activeUsers: 1500, newUsers: 1400, subscribedUsers: 1000 };
        }
  
        // Update the chart with the new data
        this.chart.updateOptions({
          series: [this.chartData.activeUsers, this.chartData.newUsers, this.chartData.subscribedUsers]
        });
      },
      renderChart() {
        this.chart = new ApexCharts(this.$refs.userOverviewDonutChart, this.options);
        this.chart.render();
      }
    },
    mounted() {
      this.renderChart();
    },
    beforeDestroy() {
      if (this.chart) {
        this.chart.destroy();
      }
    }
  };
  </script>