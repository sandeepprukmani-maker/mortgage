<template>
    <div class="col-lg-4">
      <div class="shadow-7 p-0 radius-12 bg-base overflow-hidden">
        <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between py-12 px-20 border-bottom border-neutral-200">
          <h6 class="mb-0 fw-bold text-lg">Response Time</h6>
          <div>
            <select class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8">
              <option>Yearly</option>
              <option>Monthly</option>
              <option>Weekly</option>
              <option>Today</option>
            </select>
          </div>
        </div>
        <div class="card-body p-20">
          <div class="shadow-7 p-24 radius-12 bg-base h-100">
            <div class="text-center">
              <div class="position-relative">
                <div id="semiCircleGaugeTwo" ref="semiCircleGaugeTwo" class="big-semi-circle-gauge d-flex justify-content-center"></div>
                <span
                  class="w-90-px h-90-px rounded-circle bg-neutral-50 d-flex justify-content-center align-items-center position-absolute start-50 translate-middle-x top-50">
                  <img src="@/assets/images/homeThirteen/icon/time-icon.svg" alt="Icon" />
                </span>
              </div>
              <h3 class="mt-40 mb-0">454h</h3>
              <span class="text-neutral-800 mt-4">1 hrs : 22 mins</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts';
  
  export default {
    name: 'ResponseTimeChart',
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
  
      const chart = new ApexCharts(this.$refs.semiCircleGaugeTwo, options);
      chart.render();
    },
  };
  </script>
  