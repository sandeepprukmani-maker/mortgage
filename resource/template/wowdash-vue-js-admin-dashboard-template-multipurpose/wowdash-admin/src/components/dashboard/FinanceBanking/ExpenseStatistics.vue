<template>
  <div class="col-md-6">
    <div class="card radius-16 h-100">
      <div class="card-header">
        <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
          <h6 class="mb-2 fw-bold text-lg mb-0">Expense Statistics</h6>
          <select class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8">
            <option>Today</option>
            <option>Weekly</option>
            <option>Monthly</option>
            <option>Yearly</option>
          </select>
        </div>
      </div>
      <div class="card-body">
        <div id="expenseStatistics" class="apexcharts-tooltip-z-none d-flex justify-content-center"></div>
      </div>
    </div>
  </div>
</template>

<script>
import ApexCharts from "apexcharts";

export default {
  name: "ExpenseStatisticsChart",
  mounted() {
    this.renderChart();
  },
  methods: {
    renderChart() {
      const options = {
        series: [30, 30, 30, 30],
        chart: {
          height: 240,
          type: "pie",
        },
        labels: ["Entertainment", "Bill Expense", "Others", "Investment"],
        colors: ["#02BCAF", "#F0437D", "#1C52F6", "#43DCFF"],
        legend: {
          show: true,
        },
        responsive: [
          {
            breakpoint: 480,
            options: {
              chart: {
                width: 200,
              },
              legend: {
                position: "bottom",
              },
            },
          },
        ],
      };

      const chart = new ApexCharts(
        document.querySelector("#expenseStatistics"),
        options
      );
      chart.render();
    },
  },
};
</script>