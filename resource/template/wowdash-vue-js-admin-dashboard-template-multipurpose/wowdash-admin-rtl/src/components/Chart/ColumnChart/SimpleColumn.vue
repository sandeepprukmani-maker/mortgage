<template>
    <div class="col-md-6">
      <div class="card h-100 p-0">
        <div class="card-header border-bottom bg-base py-16 px-24">
          <h6 class="text-lg fw-semibold mb-0">Simple Column</h6>
        </div>
        <div class="card-body p-24">
          <div id="upDownBarchart"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from "apexcharts";
  
  export default {
    name: "SimpleColumnChart",
    mounted() {
      this.renderChart();
    },
    methods: {
      renderChart() {
        const options = {
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
        };
        const chart = new ApexCharts(document.querySelector("#upDownBarchart"), options);
        chart.render();
      },
    },
  };
  </script>