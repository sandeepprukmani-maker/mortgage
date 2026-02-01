<template>
    <div class="col-lg-4">
      <div class="shadow-7 p-20 radius-12 bg-base h-100">
        <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
          <h6 class="mb-2 fw-bold text-lg">Ticket Priority</h6>
        </div>
        <div class="position-relative">
          <div id="statisticBarChart" class="text-style"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts';
  
  export default {
    name: 'TicketPriority',
    mounted() {
      const options = {
        series: [{
          name: 'Ticket',
          data: [6200, 5200, 4200, 3200]
        }],
        chart: {
          type: 'bar',
          height: 270,
          toolbar: {
            show: false
          }
        },
        plotOptions: {
          bar: {
            borderRadius: 4,
            horizontal: true,
            distributed: true,
            barHeight: '22px'
          }
        },
        dataLabels: {
          enabled: false
        },
        grid: {
          show: true,
          borderColor: '#ddd',
          strokeDashArray: 0,
          position: 'back',
          xaxis: {
            lines: { show: false }
          },
          yaxis: {
            lines: { show: false }
          }
        },
        xaxis: {
          categories: ['High', 'Medium', 'Low', 'Urgent'],
          labels: {
            formatter: function (value) {
              return (value / 1000).toFixed(0) + 'k';
            }
          }
        },
        legend: {
          show: false
        },
        fill: {
          type: 'gradient',
          gradient: {
            shade: 'light',
            type: 'horizontal',
            shadeIntensity: 0.5,
            gradientToColors: ['#C98BFF', '#FFDC90', '#94FF9B', '#FFAC89'],
            inverseColors: false,
            opacityFrom: 1,
            opacityTo: 1,
            stops: [0, 100]
          }
        },
        colors: [
          '#8501F8',
          '#FF9F29',
          '#00D40E',
          '#F84B01',
        ]
      };
  
      const chart = new ApexCharts(document.querySelector("#statisticBarChart"), options);
      chart.render();
    }
  };
  </script>
  