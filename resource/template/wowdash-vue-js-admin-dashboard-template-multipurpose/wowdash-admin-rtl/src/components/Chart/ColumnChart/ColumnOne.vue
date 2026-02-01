<template>
    <div class="col-md-6">
      <div class="card h-100 p-0">
        <div class="card-header border-bottom bg-base py-16 px-24">
          <h6 class="text-lg fw-semibold mb-0">Column Charts</h6>
        </div>
        <div class="card-body p-24">
          <div id="columnChart"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts';
  
  export default {
    name: 'ColumnChart',
    mounted() {
      this.renderChart();
    },
    methods: {
      renderChart() {
        const options = {
          series: [{
              name: 'Net Profit',
              data: [20000, 16000, 14000, 25000, 45000, 18000, 28000, 11000, 26000, 48000, 18000, 22000]
          },{
              name: 'Revenue',
              data: [15000, 18000, 19000, 20000, 35000, 20000, 18000, 13000, 18000, 38000, 14000, 16000]
          }],
          colors: ['#487FFF', '#FF9F29'],
          labels: ['Active', 'New', 'Total'],
          legend: {
            show: false 
          },
          chart: {
            type: 'bar',
            height: 264,
            toolbar: {
              show: false
            },
          },
          grid: {
            show: true,
            borderColor: '#D1D5DB',
            strokeDashArray: 4, // Use a number for dashed style
            position: 'back',
          },
          plotOptions: {
            bar: {
              borderRadius: 4,
              columnWidth: 10,
            },
          },
          dataLabels: {
            enabled: false
          },
          stroke: {
            show: true,
            width: 2,
            colors: ['transparent']
          },
          xaxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
          },
          yaxis: {
            categories: ['0', '5000', '10,000', '20,000', '30,000', '50,000', '60,000', '60,000', '70,000', '80,000', '90,000', '100,000'],
            labels: {
              formatter: function (value) {
                return (value / 1000).toFixed(0) + 'k';
              }
            }
          },
          tooltip: {
            y: {
              formatter: function (value) {
                return value / 1000 + 'k';
              }
            }
          },
          fill: {
            opacity: 1,
            width: 18,
          },
        };
  
        const chart = new ApexCharts(document.querySelector("#columnChart"), options);
        chart.render();
      }
    }
  }
  </script>
  