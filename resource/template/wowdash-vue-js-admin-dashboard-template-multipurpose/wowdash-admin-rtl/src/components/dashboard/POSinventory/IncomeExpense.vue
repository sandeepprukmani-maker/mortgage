<template>
    <div class="col-xxl-8">
      <div class="card h-100">
        <div class="card-body p-24 mb-8">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
            <h6 class="mb-2 fw-bold text-lg mb-0">Income Vs Expense</h6>
            <select class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8">
              <option>Yearly</option>
              <option>Monthly</option>
              <option>Weekly</option>
              <option>Today</option>
            </select>
          </div>
          <ul class="d-flex flex-wrap align-items-center justify-content-center my-3 gap-24">
            <li class="d-flex flex-column gap-1">
              <div class="d-flex align-items-center gap-2">
                <span class="w-8-px h-8-px rounded-pill bg-primary-600"></span>
                <span class="text-secondary-light text-sm fw-semibold">Income</span>
              </div>
              <div class="d-flex align-items-center gap-8">
                <h6 class="mb-0">$26,201</h6>
                <span class="text-success-600 d-flex align-items-center gap-1 text-sm fw-bolder">
                  10%
                  <i class="ri-arrow-up-s-fill d-flex"></i>
                </span>
              </div>
            </li>
            <li class="d-flex flex-column gap-1">
              <div class="d-flex align-items-center gap-2">
                <span class="w-8-px h-8-px rounded-pill bg-warning-600"></span>
                <span class="text-secondary-light text-sm fw-semibold">Expenses</span>
              </div>
              <div class="d-flex align-items-center gap-8">
                <h6 class="mb-0">$18,120</h6>
                <span class="text-danger-600 d-flex align-items-center gap-1 text-sm fw-bolder">
                  10%
                  <i class="ri-arrow-down-s-fill d-flex"></i>
                </span>
              </div>
            </li>
          </ul>
          <div id="incomeExpense" class="apexcharts-tooltip-style-1">
            <apexchart
              width="100%"
              height="270"
              type="area"
              :options="chartOptions"
              :series="chartSeries"
            />
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from "apexcharts";
  import VueApexCharts from "vue3-apexcharts";
  
  export default {
    name: "IncomeExpenseChart",
    components: {
      apexchart: VueApexCharts,
    },
    data() {
      const color1 = "#487FFF";
      const color2 = "#FF9F29";
  
      return {
        chartSeries: [
          {
            name: "income",
            data: [48, 35, 50, 32, 48, 40, 55, 50, 60],
          },
          {
            name: "Expenses",
            data: [12, 20, 15, 26, 22, 30, 25, 35, 25],
          },
        ],
        chartOptions: {
          legend: {
            show: false,
          },
          chart: {
            type: "area",
            toolbar: {
              show: false,
            },
          },
          dataLabels: {
            enabled: false,
          },
          stroke: {
            curve: "smooth",
            width: 3,
            colors: [color1, color2],
            lineCap: "round",
          },
          grid: {
            show: true,
            borderColor: "#D1D5DB",
            strokeDashArray: 1,
            position: "back",
            xaxis: {
              lines: {
                show: false,
              },
            },
            yaxis: {
              lines: {
                show: true,
              },
            },
            row: {
              colors: undefined,
              opacity: 0.5,
            },
            column: {
              colors: undefined,
              opacity: 0.5,
            },
            padding: {
              top: -20,
              right: 0,
              bottom: -10,
              left: 0,
            },
          },
          colors: [color1, color2],
          fill: {
            type: "gradient",
            colors: [color1, color2],
            gradient: {
              shade: "light",
              type: "vertical",
              shadeIntensity: 0.5,
              gradientToColors: [undefined, `${color2}00`],
              inverseColors: false,
              opacityFrom: [0.4, 0.6],
              opacityTo: [0.3, 0.3],
              stops: [0, 100],
            },
          },
          markers: {
            colors: [color1, color2],
            strokeWidth: 3,
            size: 0,
            hover: {
              size: 10,
            },
          },
          xaxis: {
            categories: [
              "Jan",
              "Feb",
              "Mar",
              "Apr",
              "May",
              "Jun",
              "Jul",
              "Aug",
              "Sep",
              "Oct",
              "Nov",
              "Dec",
            ],
            tooltip: {
              enabled: false,
            },
            labels: {
              formatter: (value) => value,
              style: {
                fontSize: "14px",
              },
            },
          },
          yaxis: {
            min:0,
            max:70,
            labels: {
              formatter: (value) => "$" + value + "k",
              style: {
                fontSize: "14px",
              },
            },
          },
          tooltip: {
            x: {
              format: "dd/MM/yy HH:mm",
            },
          },
        },
      };
    },
  };
  </script>
  