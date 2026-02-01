<template>
    <div class="col-xxl-6">
      <div class="card h-100 radius-8 border-0">
        <div class="card-body p-24">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between mb-20">
            <h6 class="mb-2 fw-bold text-lg">Coin Analytics</h6>
            <div class="border radius-4 px-3 py-2 pe-0 d-flex align-items-center gap-1 text-sm text-secondary-light">
              Currency:
              <select class="form-select form-select-sm w-auto bg-base border-0 text-primary-light fw-semibold text-sm">
                <option>USD</option>
                <option>BDT</option>
                <option>RUP</option>
              </select>
            </div>
          </div>
  
          <div v-for="(coin, index) in coins" :key="index" class="d-flex flex-wrap align-items-center justify-content-between gap-2 bg-neutral-200 px-8 py-8 radius-4 mb-16">
            <div class="d-flex flex-wrap align-items-center justify-content-between gap-2">
              <img :src="coin.imgSrc" alt="" class="w-36-px h-36-px rounded-circle flex-shrink-0">
              <div class="flex-grow-1">
                <h6 class="text-md mb-0">{{ coin.name }}</h6>
              </div>
            </div>
            <h6 class="text-md fw-medium mb-0">{{ coin.price }}</h6>
            <span :class="coin.changeClass" class="text-md fw-medium">{{ coin.change }}</span>
            <div :id="'marker' + coin.id + 'Chart'" class="remove-tooltip-title rounded-tooltip-value"></div>
          </div>
  
        </div>
      </div>
    </div>
  </template>
  
  <script>
import { ref, onMounted } from 'vue';
import ApexCharts from 'apexcharts';

import crypto1 from '@/assets/images/currency/crypto-img1.png'
import crypto2 from '@/assets/images/currency/crypto-img2.png'
import crypto3 from '@/assets/images/currency/crypto-img3.png'
import crypto4 from '@/assets/images/currency/crypto-img4.png'
import crypto5 from '@/assets/images/currency/crypto-img5.png'

export default {
  data() {
    return {
      coins: [
        { id: 'Bitcoin', name: 'Bitcoin', price: '$55,000.00', change: '+3.85%', changeClass: 'text-success-main', imgSrc: crypto1 },
        { id: 'Ethereum', name: 'Ethereum', price: '$55,000.00', change: '-2.85%', changeClass: 'text-danger-main', imgSrc: crypto2 },
        { id: 'Solana', name: 'Solana', price: '$55,000.00', change: '+3.85%', changeClass: 'text-success-main', imgSrc: crypto3 },
        { id: 'Litecoin', name: 'Litecoin', price: '$55,000.00', change: '+3.85%', changeClass: 'text-success-main', imgSrc: crypto4 },
        { id: 'Dogecoin', name: 'Dogecoin', price: '$15,000.00', change: '-2.85%', changeClass: 'text-danger-main', imgSrc: crypto5 },
        { id: 'Crypto', name: 'Crypto', price: '$15,000.00', change: '-2.85%', changeClass: 'text-danger-main', imgSrc: crypto1 }
      ]
    };
  },
  methods: {
    createChart(chartId, chartColor) {
      let currentYear = new Date().getFullYear();

      var options = {
        series: [
          {
            name: 'series1',
            data: [35, 45, 38, 41, 36, 43, 37, 55, 40],
          },
        ],
        chart: {
          type: 'area',
          width: 100,
          height: 42,
          sparkline: {
            enabled: true // Remove whitespace
          },
          toolbar: {
            show: false
          },
          padding: {
            left: 0,
            right: 0,
            top: 0,
            bottom: 0
          }
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
          curve: 'smooth',
          width: 2,
          colors: [chartColor],
          lineCap: 'round'
        },
        grid: {
          show: true,
          borderColor: 'transparent',
          strokeDashArray: 0,
          position: 'back',
          xaxis: {
            lines: {
              show: false
            }
          },   
          yaxis: {
            lines: {
              show: false
            }
          },  
          row: {
            colors: undefined,
            opacity: 0.5
          },  
          column: {
            colors: undefined,
            opacity: 0.5
          },  
          padding: {
            top: -3,
            right: 0,
            bottom: 0,
            left: 0
          },  
        },
        fill: {
          type: 'gradient',
          colors: [chartColor], // Set the starting color (top color) here
          gradient: {
            shade: 'light', // Gradient shading type
            type: 'vertical',  // Gradient direction (vertical)
            shadeIntensity: 0.5, // Intensity of the gradient shading
            gradientToColors: [`${chartColor}00`], // Bottom gradient color (with transparency)
            inverseColors: false, // Do not invert colors
            opacityFrom: .75, // Starting opacity
            opacityTo: 0.3,  // Ending opacity
            stops: [0, 100],
          },
        },
        markers: {
          colors: [chartColor],
          strokeWidth: 2,
          size: 0,
          hover: {
            size: 8
          }
        },
        xaxis: {
          labels: {
            show: false
          },
          categories: [`Jan ${currentYear}`, `Feb ${currentYear}`, `Mar ${currentYear}`, `Apr ${currentYear}`, `May ${currentYear}`, `Jun ${currentYear}`, `Jul ${currentYear}`, `Aug ${currentYear}`, `Sep ${currentYear}`, `Oct ${currentYear}`, `Nov ${currentYear}`, `Dec ${currentYear}`],
          tooltip: {
            enabled: false,
          },
        },
        yaxis: {
          labels: {
            show: false
          }
        },
        tooltip: {
          x: {
            format: 'dd/MM/yy HH:mm'
          },
        },
      };

      var chart = new ApexCharts(document.querySelector(`#${chartId}`), options);
      chart.render();
    }
  },
  mounted() {
    this.coins.forEach(coin => {
      // Change the logic here to check the coin's change value
      const chartColor = coin.change.includes('+') ? '#45B369' : '#EF4A00';
      this.createChart('marker' + coin.id + 'Chart', chartColor);
    });
  }
};
</script>

