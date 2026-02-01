<template>
    <div class="col-xxl-4 col-md-6">
      <div class="shadow-7 p-24 radius-12 bg-base h-100">
        <div class="text-center">
          <div class="position-relative">
            <div
              id="semiCircleGaugeTwo"
              ref="gaugeChart"
              class="big-semi-circle-gauge d-flex justify-content-center"
            ></div>
            <span
              class="w-90-px h-90-px rounded-circle bg-primary-50 d-flex justify-content-center align-items-center position-absolute start-50 translate-middle-x top-50"
            >
              <img src="@/assets/images/home-twelve/icons/home.png" alt="Home Icon" />
            </span>
          </div>
          <h3 class="mt-40 mb-0">35</h3>
          <span class="text-neutral-800 mt-4">Available Room Today</span>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts';
  
  export default {
    name: 'AvailableRoomCard',
    mounted() {
      const options = {
        series: [75],
        chart: {
          width: 400,
          height: 300,
          type: 'radialBar',
          sparkline: {
            enabled: true,
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
              background: '#E3E6E9',
              strokeWidth: '70%',
            },
            hollow: {
              size: '70%',
            },
            dataLabels: {
              show: false,
              value: {
                fontSize: '22px',
                fontWeight: 600,
                color: '#487FFF',
                offsetY: 16,
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
      };
  
      const chart = new ApexCharts(this.$refs.gaugeChart, options);
      chart.render();
    },
  };
  </script>
  