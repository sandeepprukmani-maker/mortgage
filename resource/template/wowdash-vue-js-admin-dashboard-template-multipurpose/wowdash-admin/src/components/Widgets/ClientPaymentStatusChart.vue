<template>
  <div class="col-xxl-4 col-lg-6">
    <div class="card h-100 border shadow-none radius-8 border-0">
      <div class="card-body p-24">
        <h6 class="mb-2 fw-bold text-lg">Client Payment Status</h6>
        <span class="text-sm fw-medium text-secondary-light">Weekly Report</span>

        <ul class="d-flex flex-wrap align-items-center justify-content-center mt-32">
          <li class="d-flex align-items-center gap-2 me-28">
            <span class="w-12-px h-12-px rounded-circle bg-success-main"></span>
            <span class="text-secondary-light text-sm fw-medium">Paid: 500</span>
          </li>
          <li class="d-flex align-items-center gap-2 me-28">
            <span class="w-12-px h-12-px rounded-circle bg-info-main"></span>
            <span class="text-secondary-light text-sm fw-medium">Pending: 500</span>
          </li>
          <li class="d-flex align-items-center gap-2">
            <span class="w-12-px h-12-px rounded-circle bg-warning-main"></span>
            <span class="text-secondary-light text-sm fw-medium">Overdue: 1500</span>
          </li>
        </ul>

        <div class="mt-40">
          <div id="paymentStatusChart" class="margin-16-minus"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted } from 'vue';
import ApexCharts from 'apexcharts';

export default {
  name: 'ClientPaymentStatus',
  setup() {
    onMounted(() => {
      const options = {
        series: [
          { name: 'Net Profit', data: [44, 100, 40, 56, 30, 58, 50] },
          { name: 'Revenue', data: [90, 140, 80, 125, 70, 140, 110] },
          { name: 'Free Cash', data: [60, 120, 60, 90, 50, 95, 90] }
        ],
        colors: ['#45B369', '#144bd6', '#FF9F29'],
        labels: ['Active', 'New', 'Total'],
        legend: {
          show: false
        },
        chart: {
          type: 'bar',
          height: 350,
          toolbar: {
            show: false
          },
        },
        grid: {
          show: true,
          borderColor: '#D1D5DB',
          strokeDashArray: 4,
          position: 'back',
        },
        plotOptions: {
          bar: {
            borderRadius: 4,
            columnWidth: 8,
          },
        },
        dataLabels: {
          enabled: false
        },
        states: {
          hover: {
            filter: {
              type: 'none'
            }
          }
        },
        stroke: {
          show: true,
          width: 0,
          colors: ['transparent']
        },
        xaxis: {
          categories: ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun'],
        },
        yaxis: {
          min:0,
          max:160,
          tickAmount:4,
          categories: ['0', '10,000', '20,000', '30,000', '50,000', '1,00,000', '1,00,000'],
        },
        fill: {
          opacity: 1,
          width: 18,
        },
      };

      const chart = new ApexCharts(document.querySelector("#paymentStatusChart"), options);
      chart.render();
    });
  }
};
</script>