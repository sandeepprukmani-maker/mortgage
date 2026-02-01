<template>
  <div class="col-xxl-8">
    <div class="card radius-8 border-0 p-20">
      <div class="row gy-4">
        <div class="col-xxl-4">
          <!-- Total Students -->
          <div class="card p-3 radius-8 shadow-none bg-gradient-dark-start-1 mb-12">
            <div class="card-body p-0">
              <div class="d-flex flex-wrap align-items-center justify-content-between gap-1 mb-0">
                <div class="d-flex align-items-center gap-2 mb-12">
                  <span class="mb-0 w-48-px h-48-px bg-base text-pink text-2xl flex-shrink-0 d-flex justify-content-center align-items-center rounded-circle h6">
                    <i class="ri-group-fill"></i>
                  </span>
                  <div>
                    <span class="mb-0 fw-medium text-secondary-light text-lg">Total Students</span>
                  </div>
                </div>
              </div>
              <div class="d-flex align-items-center justify-content-between flex-wrap gap-8">
                <h5 class="fw-semibold mb-0">15,000</h5>
                <p class="text-sm mb-0 d-flex align-items-center gap-8">
                  <span class="text-white px-1 rounded-2 fw-medium bg-success-main text-sm">+2.5k</span>
                  This Month
                </p>
              </div>
            </div>
          </div>

          <!-- Total Courses -->
          <div class="card p-3 radius-8 shadow-none bg-gradient-dark-start-2 mb-12">
            <div class="card-body p-0">
              <div class="d-flex flex-wrap align-items-center justify-content-between gap-1 mb-0">
                <div class="d-flex align-items-center gap-2 mb-12">
                  <span class="mb-0 w-48-px h-48-px bg-base text-purple text-2xl flex-shrink-0 d-flex justify-content-center align-items-center rounded-circle h6">
                    <i class="ri-youtube-fill"></i>
                  </span>
                  <div>
                    <span class="mb-0 fw-medium text-secondary-light text-lg">Total Courses</span>
                  </div>
                </div>
              </div>
              <div class="d-flex align-items-center justify-content-between flex-wrap gap-8">
                <h5 class="fw-semibold mb-0">420</h5>
                <p class="text-sm mb-0 d-flex align-items-center gap-8">
                  <span class="text-white px-1 rounded-2 fw-medium bg-success-main text-sm">+30</span>
                  This Month
                </p>
              </div>
            </div>
          </div>

          <!-- Overall Revenue -->
          <div class="card p-3 radius-8 shadow-none bg-gradient-dark-start-3 mb-0">
            <div class="card-body p-0">
              <div class="d-flex flex-wrap align-items-center justify-content-between gap-1 mb-0">
                <div class="d-flex align-items-center gap-2 mb-12">
                  <span class="mb-0 w-48-px h-48-px bg-base text-info text-2xl flex-shrink-0 d-flex justify-content-center align-items-center rounded-circle h6">
                    <i class="ri-money-dollar-circle-fill"></i>
                  </span>
                  <div>
                    <span class="mb-0 fw-medium text-secondary-light text-lg">Overall Revenue</span>
                  </div>
                </div>
              </div>
              <div class="d-flex align-items-center justify-content-between flex-wrap gap-8">
                <h5 class="fw-semibold mb-0">$50,000</h5>
                <p class="text-sm mb-0 d-flex align-items-center gap-8">
                  <span class="text-white px-1 rounded-2 fw-medium bg-success-main text-sm">+1.5k</span>
                  This Month
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Chart & Info -->
        <div class="col-xxl-8">
          <div class="card-body p-0">
            <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
              <h6 class="mb-2 fw-bold text-lg">Average Enrollment Rate</h6>
              <div>
                <select class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8">
                  <option>Yearly</option>
                  <option>Monthly</option>
                  <option>Weekly</option>
                  <option>Today</option>
                </select>
              </div>
            </div>

            <ul class="d-flex flex-wrap align-items-center justify-content-center mt-3 gap-3">
              <li class="d-flex align-items-center gap-2">
                <span class="w-12-px h-12-px rounded-circle bg-primary-600"></span>
                <span class="text-secondary-light text-sm fw-semibold">Paid Course:
                  <span class="text-primary-light fw-bold">350</span>
                </span>
              </li>
              <li class="d-flex align-items-center gap-2">
                <span class="w-12-px h-12-px rounded-circle bg-success-main"></span>
                <span class="text-secondary-light text-sm fw-semibold">Free Course:
                  <span class="text-primary-light fw-bold">70</span>
                </span>
              </li>
            </ul>

            <div class="mt-40">
              <div id="enrollmentChart" class="apexcharts-tooltip-style-1"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ApexCharts from 'apexcharts';

export default {
  name: 'DashboardStats',
  mounted() {
    this.createChartTwo('enrollmentChart', '#45B369', '#487fff');
  },
  methods: {
    createChartTwo(chartId, color1, color2) {
      const options = {
        series: [
          { name: 'series1', data: [48, 35, 55, 32, 48, 30, 55, 50, 57] },
          { name: 'series2', data: [12, 20, 15, 26, 22, 60, 40, 48, 25] },
        ],
        legend: { show: false },
        chart: {
          type: 'area',
          width: '100%',
          height: 270,
          toolbar: { show: false },
          padding: { left: 0, right: 0, top: 0, bottom: 0 }
        },
        dataLabels: { enabled: false },
        stroke: {
          curve: 'smooth',
          width: 3,
          colors: [color1, color2],
          lineCap: 'round'
        },
        grid: {
          show: true,
          borderColor: '#D1D5DB',
          strokeDashArray: 1,
          position: 'back',
          xaxis: { lines: { show: false } },
          yaxis: { lines: { show: true } },
          row: { opacity: 0.5 },
          column: { opacity: 0.5 },
          padding: { top: -20, right: 0, bottom: -10, left: 0 }
        },
        colors: [color1, color2],
        fill: {
          type: 'gradient',
          colors: [color1, color2],
          gradient: {
            shade: 'light',
            type: 'vertical',
            shadeIntensity: 0.5,
            gradientToColors: [undefined, `${color2}00`],
            inverseColors: false,
            opacityFrom: [0.4, 0.4],
            opacityTo: [0.3, 0.3],
            stops: [0, 100]
          }
        },
        markers: {
          colors: [color1, color2],
          strokeWidth: 3,
          size: 0,
          hover: { size: 10 }
        },
        xaxis: {
          categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
          labels: {
            formatter: value => value,
            style: { fontSize: "14px" }
          },
          tooltip: { enabled: false }
        },
        yaxis: {
          min:0,
          max:70,
          labels: {
            formatter: value => "$" + value + "k",
            style: { fontSize: "14px" }
          }
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
