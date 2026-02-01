<template>
    <div class="col-xxl-4">
      <div class="card h-100 radius-8 border">
        <div class="card-body p-24">
          <h6 class="mb-12 fw-bold text-lg mb-0">Recent Orders</h6>
          <div class="d-flex align-items-center gap-2">
            <h6 class="fw-semibold mb-0">$27,200</h6>
            <p class="text-sm mb-0">
              <span class="bg-success-focus border border-success px-8 py-2 rounded-pill fw-semibold text-success-main text-sm d-inline-flex align-items-center gap-1">
                10%
                <iconify-icon icon="iconamoon:arrow-up-2-fill" class="icon"></iconify-icon>
              </span>
              Increases
            </p>
          </div>
          <div id="recent-orders" class="mt-28"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from "apexcharts";
  import { onMounted } from "vue";
  
  export default {
    name: "RecentOrders",
    methods: {
      createChartTwo(chartId, chartColor) {
        var options = {
          series: [
            {
              name: "This Day",
              data: [18, 25, 20, 35, 25, 55, 45, 50, 40],
            },
          ],
          chart: {
            type: "area",
            width: "100%",
            height: 360,
            sparkline: {
              enabled: false, // Remove whitespace
            },
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
            width: 4,
            colors: [chartColor],
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
              top: -30,
              right: 0,
              bottom: -10,
              left: 0,
            },
          },
          colors: [chartColor], // Set color for series
          fill: {
            type: "gradient",
            colors: [chartColor], // Set the starting color (top color) here
            gradient: {
              shade: "light", // Gradient shading type
              type: "vertical", // Gradient direction (vertical)
              shadeIntensity: 0.5, // Intensity of the gradient shading
              gradientToColors: [`${chartColor}00`], // Bottom gradient color (with transparency)
              inverseColors: false, // Do not invert colors
              opacityFrom: 0.6, // Starting opacity
              opacityTo: 0.3, // Ending opacity
              stops: [0, 100],
            },
          },
          markers: {
            colors: [chartColor],
            strokeWidth: 3,
            size: 0,
            hover: {
              size: 10,
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
            labels: {
              show: false,
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
    mounted() {
      this.createChartTwo("recent-orders", "#487fff");
    },
  };
  </script>
  