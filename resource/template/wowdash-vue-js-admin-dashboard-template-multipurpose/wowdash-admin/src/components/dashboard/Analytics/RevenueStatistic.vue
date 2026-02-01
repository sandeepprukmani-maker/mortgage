<template>
    <div class="col-xxl-6">
      <div class="card h-100">
        <div class="card-body p-24 mb-8">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
            <h6 class="mb-2 fw-bold text-lg mb-0">Revenue Statistic</h6>
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
                <span class="text-secondary-light text-sm fw-semibold">Profit</span>
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
                <span class="w-8-px h-8-px rounded-pill bg-lilac-600"></span>
                <span class="text-secondary-light text-sm fw-semibold">Loss</span>
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
          <div id="revenueChart" class="apexcharts-tooltip-style-1"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from "apexcharts";
  
  export default {
    name: "RevenueStatistic",
    mounted() {
      this.createChartTwo("revenueChart", "#CD20F9", "#6593FF");
    },
    methods: {
      createChartTwo(chartId, color1, color2) {
        const options = {
          series: [
            {
              name: "Profit",
              data: [6, 20, 15, 48, 28, 55, 28, 52, 25, 32, 15, 25],
            },
            {
              name: "Loss",
              data: [0, 8, 4, 36, 16, 42, 16, 40, 12, 24, 4, 12],
            },
          ],
          legend: {
            show: false,
          },
          chart: {
            type: "area",
            width: "100%",
            height: 150,
            toolbar: {
              show: false,
            },
            padding: {
              left: 0,
              right: 0,
              top: 0,
              bottom: 0,
            },
          },
          dataLabels: {
            enabled: false,
          },
          stroke: {
            curve: "smooth",
            width: 3,
            colors: [color1, color2], // Use two colors for the lines
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
          colors: [color1, color2], // Set color for series
          fill: {
            type: "gradient",
            colors: [color1, color2], // Use two colors for the gradient
            gradient: {
              shade: "light",
              type: "vertical",
              shadeIntensity: 0.5,
              gradientToColors: [undefined, `${color2}00`], // Apply transparency to both colors
              inverseColors: false,
              opacityFrom: [0.4, 0.6], // Starting opacity for both colors
              opacityTo: [0.3, 0.3], // Ending opacity for both colors
              stops: [0, 100],
            },
          },
          markers: {
            colors: [color1, color2],
            strokeWidth: 2,
            size: 0,
            hover: {
              size: 8,
            },
          },
          xaxis: {
            labels: {
              show: false,
            },
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
              formatter: function (value) {
                return value;
              },
              style: {
                fontSize: "14px",
              },
            },
          },
          yaxis: {
            tickAmount:6,
            labels: {
              formatter: function (value) {
                return "$" + value + "k";
              },
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
        };
  
        var chart = new ApexCharts(
          document.querySelector(`#${chartId}`),
          options
        );
        chart.render();
      },
    },
  };
  </script>