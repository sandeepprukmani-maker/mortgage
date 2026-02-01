<template>
    <div class="col-xxl-4">
      <div class="shadow-7 p-20 radius-12 bg-base h-100">
        <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
          <h6 class="mb-2 fw-bold text-lg">Booking Statistic</h6>
          <div>
            <select class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8">
              <option>Yearly</option>
              <option>Monthly</option>
              <option>Weekly</option>
              <option>Today</option>
            </select>
          </div>
        </div>
        <div class="position-relative">
          <div id="statisticBarChart" ref="statChart" class="text-style"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts';
  
  export default {
    name: 'BookingStatisticChart',
    mounted() {
      const options = {
        series: [
          {
            name: 'Booking',
            data: [6200, 5200, 4200, 3200, 1200],
          },
        ],
        chart: {
          type: 'bar',
          height: 270,
          toolbar: {
            show: false,
          },
        },
        plotOptions: {
          bar: {
            borderRadius: 4,
            horizontal: true,
            distributed: true,
            barHeight: '22px',
          },
        },
        dataLabels: {
          enabled: false,
        },
        grid: {
          show: true,
          borderColor: '#ddd',
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
        },
        xaxis: {
          categories: ['Booking', 'Pending', 'Finished', 'Canceled', 'Refunded'],
          labels: {
            formatter: function (value) {
              return (value / 1000).toFixed(0) + 'k';
            },
          },
        },
        legend: {
          show: false,
        },
        fill: {
          type: 'gradient',
          gradient: {
            shade: 'light',
            type: 'horizontal',
            shadeIntensity: 0.5,
            gradientToColors: [
              '#C98BFF',
              '#FFDC90',
              '#94FF9B',
              '#FFAC89',
              '#A3E2FE',
            ],
            inverseColors: false,
            opacityFrom: 1,
            opacityTo: 1,
            stops: [0, 100],
          },
        },
        colors: ['#8501F8', '#FF9F29', '#00D40E', '#F84B01', '#2FBCFC'],
      };
  
      const chart = new ApexCharts(this.$refs.statChart, options);
      chart.render();
    },
  };
  </script>
  