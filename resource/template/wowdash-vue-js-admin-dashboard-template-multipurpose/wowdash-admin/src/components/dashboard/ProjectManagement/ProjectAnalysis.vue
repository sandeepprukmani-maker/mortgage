<template>
    <div class="col-xxl-4 col-sm-6">
      <div class="card h-100 radius-8 border-0">
        <div class="card-header border-bottom bg-base py-16 px-24 d-flex align-items-center justify-content-between">
          <h6 class="text-lg fw-semibold mb-0">Project Analysis</h6>
          <div class="">
            <select class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8" v-model="selectedTimeFrame">
              <option>Yearly</option>
              <option>Monthly</option>
              <option>Weekly</option>
              <option>Today</option>
            </select>
          </div>
        </div>
        <div class="card-body p-24">
          <ul class="d-flex flex-wrap align-items-center justify-content-center">
            <li class="d-flex align-items-center gap-2 me-28">
              <span class="w-12-px h-12-px rounded-circle bg-success-main"></span>
              <span class="text-secondary-light text-sm fw-medium">Revenue</span>
            </li>
            <li class="d-flex align-items-center gap-2 me-28">
              <span class="w-12-px h-12-px rounded-circle bg-warning-main"></span>
              <span class="text-secondary-light text-sm fw-medium">Expenses</span>
            </li>
            <li class="d-flex align-items-center gap-2">
              <span class="w-12-px h-12-px rounded-circle bg-purple"></span>
              <span class="text-secondary-light text-sm fw-medium">Budgets</span>
            </li>
          </ul>
          <div class="mt-40">
            <div id="projectAnalysisChart" class="margin-16-minus"></div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts';
  import { defineComponent, onMounted, ref } from 'vue';
  
  export default defineComponent({
    name: 'ProjectAnalysis',
    setup() {
      const selectedTimeFrame = ref('Yearly');
      
      onMounted(() => {
        const options = {
          series: [
            {
              name: 'Net Profit',
              data: [44, 100, 40, 56, 30, 58, 50],
            },
            {
              name: 'Revenue',
              data: [90, 140, 80, 125, 70, 140, 110],
            },
            {
              name: 'Free Cash',
              data: [60, 120, 60, 90, 50, 95, 90],
            },
          ],
          colors: ['#45B369', '#FF9F29', '#9935FE'],
          labels: ['Active', 'New', 'Total'],
          legend: {
            show: false,
          },
          chart: {
            type: 'bar',
            height: 350,
            toolbar: {
              show: false,
            },
          },
          grid: {
            show: true,
            borderColor: '#D1D5DB',
            strokeDashArray: 4,
            position: 'back',
          },
          plotOptions: {
            bar: {
              borderRadius: 4,
              columnWidth: 8,
            },
          },
          dataLabels: {
            enabled: false,
          },
          states: {
            hover: {
              filter: {
                type: 'none',
              },
            },
          },
          stroke: {
            show: true,
            width: 0,
            colors: ['transparent'],
          },
          xaxis: {
            categories: ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun'],
          },
          yaxis: {
            min:0,
            max:160,
            tickAmount:4,
            categories: ['0', '10,000', '20,000', '30,000', '50,000', '1,00,000', '1,00,000'],
          },
          fill: {
            opacity: 1,
            width: 18,
          },
        };
  
        const chart = new ApexCharts(document.querySelector('#projectAnalysisChart'), options);
        chart.render();
      });
  
      return {
        selectedTimeFrame,
      };
    },
  });
  </script>