<template>
    <div class="col-xxl-4 col-xl-6">
      <div class="card h-100">
        <div class="card-body p-24">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
            <h6 class="mb-2 fw-bold text-lg mb-0">Average Daily Sales</h6>
            <select class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8">
              <option>Yearly</option>
              <option>Monthly</option>
              <option>Weekly</option>
              <option>Today</option>
            </select>
          </div>
          <h6 class="text-center my-20">$27,500.00</h6>
          <div id="barChart" class="barChart"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts';
  
  export default {
    name: 'AverageDailySales',
    mounted() {
      this.createBarChart();
    },
    methods: {
      createBarChart() {
        const options = {
          series: [{
            name: "Sales",
            data: [
              { x: 'Sun', y: 15 },
              { x: 'Mon', y: 12 },
              { x: 'Tue', y: 18 },
              { x: 'Wed', y: 20 },
              { x: 'Thu', y: 13 },
              { x: 'Fri', y: 16 },
              { x: 'Sat', y: 6 },
            ]
          }],
          chart: {
            type: 'bar',
            height: 200,
            toolbar: {
              show: false
            },
          },
          plotOptions: {
            bar: {
              borderRadius: 6,
              horizontal: false,
              columnWidth: 24,
              columnWidth: '40%',
              endingShape: 'rounded',
            }
          },
          dataLabels: {
            enabled: false
          },
          fill: {
            type: 'gradient',
            colors: ['#dae5ff'],
            gradient: {
              shade: 'light',
              type: 'vertical',
              shadeIntensity: 0.5,
              gradientToColors: ['#dae5ff'],
              inverseColors: false,
              opacityFrom: 1,
              opacityTo: 1,
              stops: [0, 100],
            },
          },
          grid: {
            show: false,
            borderColor: '#D1D5DB',
            strokeDashArray: 4,
            position: 'back',
            padding: {
              top: -10,
              right: -10,
              bottom: -10,
              left: -10
            }
          },
          xaxis: {
            type: 'category',
            categories: ['2hr', '4hr', '6hr', '8hr', '10hr', '12hr', '14hr']
          },
          yaxis: {
            show: false,
          },
        };
  
        var chart = new ApexCharts(
          document.querySelector("#barChart"),
          options
        );
        chart.render();
      },
    },
  };
  </script>