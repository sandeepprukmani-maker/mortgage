<template>
        <div class="col-xxl-12 col-sm-6">
          <div class="card h-100 radius-8 border-0 overflow-hidden">
            <div class="card-body p-24">
              <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
                <h6 class="mb-2 fw-bold text-lg">Customer Overview</h6>
                <div>
                  <select v-model="selectedTimeframe" class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8">
                    <option>Yearly</option>
                    <option>Monthly</option>
                    <option>Weekly</option>
                    <option>Today</option>
                  </select>
                </div>
              </div>
  
              <div class="d-flex flex-wrap align-items-center mt-3">
                <ul class="flex-shrink-0">
                  <li v-for="(item, index) in customerData" :key="index" class="d-flex align-items-center gap-2 mb-28">
                    <span :style="{ backgroundColor: item.color }" class="w-12-px h-12-px rounded-circle"></span>
                    <span class="text-secondary-light text-sm fw-medium">{{ item.label }}: {{ item.value }}</span>
                  </li>
                </ul>
                <div id="donutChart" class="flex-grow-1 apexcharts-tooltip-z-none title-style circle-none"></div>
              </div>
  
            </div>
          </div>
        </div>
  </template>
  
  <script>
  import { ref, onMounted, watch } from 'vue';
  import ApexCharts from 'apexcharts';
  import { defineComponent } from 'vue';
  import { Icon } from "@iconify/vue";
  
  export default defineComponent({
    name: 'DashboardComponent',
    setup() {
      // Customer Data
      const customerData = ref([
        { label: 'Total', value: 500, color: '#45B369' },
        { label: 'New', value: 500, color: '#FF9F29' },
        { label: 'Active', value: 1500, color: '#487FFF' }
      ]);
  
      // Timeframe Selection
      const selectedTimeframe = ref('Yearly');
  
      // Donut Chart Data
      const options = {
        series: customerData.value.map(item => item.value),
        colors: customerData.value.map(item => item.color),
        labels: customerData.value.map(item => item.label),
        legend: {
          show: false,
        },
        chart: {
          type: 'donut',
          height: 300,
          sparkline: {
            enabled: true
          },
          margin: {
            top: -100,
            right: -100,
            bottom: -100,
            left: -100
          },
          padding: {
            top: -100,
            right: -100,
            bottom: -100,
            left: -100
          }
        },
        stroke: {
          width: 0,
        },
        dataLabels: {
          enabled: false
        },
        plotOptions: {
          pie: {
            startAngle: -90,
            endAngle: 90,
            offsetY: 10,
            customScale: 0.8,
            donut: {
              size: '70%',
              labels: {
                showAlways: true,
                show: true,
                label: 'Customer Report',
              }
            },
          }
        }
      };
  
      // Initialize the chart
      let chart = null;
  
      const renderChart = () => {
        if (chart) {
          chart.destroy();
        }
        chart = new ApexCharts(document.querySelector('#donutChart'), options);
        chart.render();
      };
  
      // Watch for changes to customer data and re-render the chart
      watch(customerData, renderChart, { deep: true });
  
      // Mount the chart when the component is mounted
      onMounted(() => {
        renderChart();
      });
  
      return {
        customerData,
        selectedTimeframe
      };
    }
  });
  </script>
  
  <style scoped>
  /* Add custom styles here if needed */
  </style>
  