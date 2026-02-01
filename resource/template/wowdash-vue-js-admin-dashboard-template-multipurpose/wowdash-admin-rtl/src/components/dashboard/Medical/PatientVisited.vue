<template>
      <!-- Patient Visited by Department -->
      <div class="col-xxl-6">
        <div class="card h-100">
          <div class="card-header">
            <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
              <h6 class="mb-2 fw-bold text-lg mb-0">Patient Visited by Depertment</h6>
            </div>
          </div>
          <div class="card-body p-24 d-flex align-items-center gap-16">
            <div id="radialMultipleBar"></div>
            <ul class="d-flex flex-column gap-12">
              <li>
                <span class="text-lg">Cardiology: <span class="text-primary-600 fw-semibold">80%</span> </span>
              </li>
              <li>
                <span class="text-lg">Psychiatry:  <span class="text-warning-600 fw-semibold">40%</span> </span>
              </li>
              <li>
                <span class="text-lg">Pediatrics: <span class="text-success-600 fw-semibold">10%</span> </span>
              </li>
            </ul>
          </div>
        </div>
      </div>
  
      <!-- Patient Visit By Gender -->
      <div class="col-xxl-6">
        <div class="card h-100">
          <div class="card-header">
            <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
              <h6 class="mb-2 fw-bold text-lg mb-0">Patient Visit By Gender</h6>
              <select class="form-select form-select-sm w-auto bg-base border-0 text-secondary-light">
                <option>This Month</option>
                <option>This Week</option>
                <option>This Year</option>
              </select>
            </div>
          </div>
          <div class="card-body p-24">
            <ul class="d-flex flex-wrap align-items-center justify-content-center my-3 gap-3">
              <li class="d-flex align-items-center gap-2">
                <span class="w-12-px h-8-px rounded-pill bg-warning-600"></span>
                <span class="text-secondary-light text-sm fw-semibold">Male: 
                  <span class="text-primary-light fw-bold">200</span>
                </span>
              </li>
              <li class="d-flex align-items-center gap-2">
                <span class="w-12-px h-8-px rounded-pill bg-success-600"></span>
                <span class="text-secondary-light text-sm fw-semibold">Female: 
                  <span class="text-primary-light fw-bold">450</span>
                </span>
              </li>
            </ul>
            <div id="paymentStatusChart" class="margin-16-minus y-value-left"></div>
          </div>
        </div>
      </div>
  </template>
  
  <script>
  import ApexCharts from 'apexcharts';
  
  export default {
    name: 'PatientDashboard',
    mounted() {
      // Multiple Radial Bar Chart
      const radialOptions = {
        series: [80, 40, 10],
        chart: {
          height: 276,
          type: 'radialBar',
        },
        colors: ['#3D7FF9', '#ff9f29', '#16a34a'],
        stroke: {
          lineCap: 'round',
        },
        plotOptions: {
          radialBar: {
            hollow: {
              size: '10%',
            },
            dataLabels: {
              name: {
                fontSize: '16px',
              },
              value: {
                fontSize: '16px',
              },
            },
            track: {
              margin: 20,
            }
          }
        },
        labels: ['Cardiology', 'Psychiatry', 'Pediatrics'],
      };
      new ApexCharts(document.querySelector("#radialMultipleBar"), radialOptions).render();
  
      // Payment Status Bar Chart
      const barOptions = {
        series: [
          {
            name: 'Net Profit',
            data: [44, 100, 40, 56, 30, 58, 50]
          },
          {
            name: 'Free Cash',
            data: [60, 120, 60, 90, 50, 95, 90]
          }
        ],
        colors: ['#45B369', '#FF9F29'],
        labels: ['Active', 'New', 'Total'],
        legend: {
          show: false
        },
        chart: {
          type: 'bar',
          height: 260,
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
        yaxis:{
          min:0,
          max:120,  
          tickAmount: 4, 
        },
        xaxis: {
          categories: ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun'],
        },
        fill: {
          opacity: 1,
          width: 18,
        },
      };
      new ApexCharts(document.querySelector("#paymentStatusChart"), barOptions).render();
    }
  };
  </script>
  
