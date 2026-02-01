<template>
    <div class="col-xxl-8">
      <div class="card h-100 radius-8 border-0">
        <div class="card-body p-24">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
            <div>
              <h6 class="mb-2 fw-bold text-lg">Revenue Statistics</h6>
              <span class="text-sm fw-medium text-secondary-light">Yearly earning overview</span>
            </div>
            <div class="">
              <select v-model="selectedTimeFrame" class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8">
                <option>Yearly</option>
                <option>Monthly</option>
                <option>Weekly</option>
                <option>Today</option>
              </select>
            </div>
          </div>
  
          <div class="mt-24 mb-24 d-flex flex-wrap">
            <div class="me-40">
              <span class="text-secondary-light text-sm mb-1">Income</span>
              <div>
                <h6 class="fw-semibold d-inline-block mb-0">${{ income }}</h6>
                <span class="text-success-main fw-bold d-inline-flex align-items-center gap-1">10% <iconify-icon icon="iconamoon:arrow-up-2-fill" class="icon"></iconify-icon></span>
              </div>
            </div>
            <div>
              <span class="text-secondary-light text-sm mb-1">Expenses</span>
              <div>
                <h6 class="fw-semibold d-inline-block mb-0">${{ expenses }}</h6>
                <span class="text-danger-main fw-bold d-inline-flex align-items-center gap-1">10% <iconify-icon icon="iconamoon:arrow-down-2-fill" class="icon"></iconify-icon></span>
              </div>
            </div>
          </div>
  
          <div id="upDownBarchart">
            <apexchart
              type="bar"
              height="263"
              :options="chartOptions"
              :series="chartSeries"
            />
          </div>
  
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from 'vue3-apexcharts';
  
  export default {
    name: "RevenueStatistics",
    components: {
      apexchart: ApexCharts,
    },
    data() {
      return {
        selectedTimeFrame: 'Yearly',
        income: '26,201',
        expenses: '18,120',
        chartOptions: {
          series: [
            {
              name: "Income",
              data: [44, 42, 57, 86, 58, 55, 70, 44, 42, 57, 86, 58, 55, 70],
            },
            {
              name: "Expenses",
              data: [-34, -22, -37, -56, -21, -35, -60, -34, -22, -37, -56, -21, -35, -60],
            },
          ],
          chart: {
            stacked: true,
            type: "bar",
            height: 263,
            fontFamily: "Poppins, sans-serif",
            toolbar: {
              show: false,
            },
          },
          colors: ["#487FFF", "#EF4A00"],
          plotOptions: {
            bar: {
              columnWidth: "8",
              borderRadius: [2],
              borderRadiusWhenStacked: "all",
            },
          },
          stroke: {
            width: [5, 5],
          },
          dataLabels: {
            enabled: false,
          },
          legend: {
            show: true,
            position: "top",
          },
          yaxis: {
            show: false,
            title: {
              text: undefined,
            },
            labels: {
              formatter: function (y) {
                return y.toFixed(0) + "";
              },
            },
          },
          xaxis: {
            show: false,
            categories: [
              "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun",
              "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"
            ],
            axisBorder: {
              show: false,
            },
            axisTicks: {
              show: false,
            },
            labels: {
              show: true,
              style: {
                colors: "#d4d7d9",
                fontSize: "10px",
                fontWeight: 500,
              },
            },
          },
          tooltip: {
            enabled: true,
            shared: true,
            intersect: false,
            theme: "dark",
            x: {
              show: false,
            },
          },
        },
      };
    },
    computed: {
      chartSeries() {
        return [
          {
            name: "Income",
            data: [44, 42, 57, 86, 58, 55, 70, 44, 42, 57, 86, 58, 55, 70],
          },
          {
            name: "Expenses",
            data: [-34, -22, -37, -56, -21, -35, -60, -34, -22, -37, -56, -21, -35, -60],
          },
        ];
      }
    }
  };
  </script>