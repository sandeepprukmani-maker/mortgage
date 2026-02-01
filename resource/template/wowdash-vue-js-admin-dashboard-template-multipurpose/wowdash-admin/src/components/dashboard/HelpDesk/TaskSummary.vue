<template>
    <div class="col-lg-8">
      <div class="shadow-7 p-20 radius-12 bg-base z-1 gradient-bg-chart position-relative h-100">
        <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between mb-3">
          <h6 class="mb-2 fw-bold text-lg">Task Summary</h6>
        </div>
        <div class="row gy-4">
          <div class="col-xxxl-3 col-sm-6" v-for="(item, index) in taskData" :key="index">
            <div :class="['radius-12 overflow-hidden p-20 position-relative z-1', item.bgClass]">
              <img
                src="@/assets/images/homeThirteen/shape/moon-shape-border.png"
                alt="Shape"
                class="position-absolute start-0 bottom-0 mb-10 z-n1"
              />
              <span class="d-block text-base mb-24">{{ item.label }}</span>
              <div class="d-flex align-items-center justify-content-between gap-3">
                <h5 class="text-base">{{ item.value }}</h5>
                <span class="opacity-25">
                  <img :src="item.icon" alt="Icon" />
                </span>
              </div>
            </div>
          </div>
        </div>
  
        <div class="mt-20 d-flex align-items-center justify-content-between gap-4 flex-wrap">
          <div>
            <span class="text-secondary-light">On Time Completion Rate</span>
            <div class="d-flex align-items-center gap-3 mt-8">
              <h5 class="mb-0">98%</h5>
              <div class="d-flex align-items-center gap-1 text-success-600 fw-semibold">
                <span class="line-height-1 d-flex"><i class="ri-arrow-right-up-line"></i></span>
                <span>2.73%</span>
              </div>
            </div>
          </div>
          <div>
            <div id="enrollmentChart" class="apexcharts-tooltip-style-1"></div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts';
  
  import icon1 from '@/assets/images/homeThirteen/icon/task-summary-icon1.svg'
  import icon2 from '@/assets/images/homeThirteen/icon/task-summary-icon2.svg'
  import icon3 from '@/assets/images/homeThirteen/icon/task-summary-icon3.svg'
  import icon4 from '@/assets/images/homeThirteen/icon/task-summary-icon4.svg'
  
  export default {
    name: 'TaskSummary',
    data() {
      return {
        taskData: [
          {
            label: 'New Resolved',
            value: '2.5k',
            icon: icon1,
            bgClass: 'bg-gradient-custom-1',
          },
          {
            label: 'Tickets In Progress',
            value: '2.5k',
            icon: icon2,
            bgClass: 'bg-gradient-custom-2',
          },
          {
            label: 'Tickets Due',
            value: '2.5k',
            icon: icon3,
            bgClass: 'bg-gradient-custom-3',
          },
          {
            label: 'Tickets Resolved',
            value: '2.5k',
            icon: icon4,
            bgClass: 'bg-gradient-custom-4',
          }
        ]
      };
    },
    mounted() {
      this.createChartTwo('enrollmentChart', '#487FFF', '#FF9F29');
    },
    methods: {
      createChartTwo(chartId, color1, color2) {
        const options = {
          series: [{
            name: 'series1',
            data: [48, 35, 55, 32, 48, 30, 55, 50, 57]
          }],
          legend: {
            show: false
          },
          chart: {
            type: 'area',
            width: 466,
            height: 86,
            toolbar: { show: false },
            dropShadow: { enabled: false }
          },
          dataLabels: { enabled: false },
          stroke: {
            curve: 'smooth',
            width: 3,
            colors: [color1, color2]
          },
          fill: {
            type: 'solid',
            opacity: 0
          },
          grid: {
            show: false
          },
          markers: {
            colors: [color1, color2],
            strokeWidth: 3,
            size: 0,
            hover: { size: 10 }
          },
          xaxis: {
            labels: { show: false },
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            tooltip: { enabled: false }
          },
          yaxis: {
            labels: { show: false }
          },
          tooltip: {
            x: { format: 'dd/MM/yy HH:mm' }
          }
        };
  
        const chart = new ApexCharts(document.querySelector(`#${chartId}`), options);
        chart.render();
      }
    }
  };
  </script>
  