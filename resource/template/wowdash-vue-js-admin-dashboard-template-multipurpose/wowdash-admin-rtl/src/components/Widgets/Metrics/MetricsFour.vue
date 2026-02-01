<template>
    <div class="mt-24">
      <div class="row row-cols-xxxl-5 row-cols-lg-3 row-cols-sm-2 row-cols-1 gy-4">
        <div v-for="(coin, index) in coins" :key="index" class="col">
          <div :class="['card shadow-none border', coin.bgClass]">
            <div class="card-body p-20">
              <div class="d-flex flex-wrap align-items-center justify-content-between gap-3">
                <img :src="coin.img" alt="" class="w-40-px h-40-px rounded-circle flex-shrink-0">
                <div class="flex-grow-1">
                  <h6 class="text-xl mb-1">{{ coin.name }}</h6>
                  <p class="fw-medium text-secondary-light mb-0">{{ coin.symbol }}</p>
                </div>
              </div>
              <div class="mt-3 d-flex flex-wrap justify-content-between align-items-center gap-1">
                <div class="">
                  <h6 class="mb-8">{{ coin.price }}</h6>
                  <span :class="coin.changeClass">{{ coin.change }}</span>
                </div>
                <div :id="coin.chartId" class="remove-tooltip-title rounded-tooltip-value"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ApexCharts from "apexcharts";
  import { ref, onMounted } from "vue";

  import crypto1 from "@/assets/images/currency/crypto-img1.png"
  import crypto2 from "@/assets/images/currency/crypto-img2.png"
  import crypto3 from "@/assets/images/currency/crypto-img3.png"
  import crypto4 from "@/assets/images/currency/crypto-img4.png"
  import crypto5 from "@/assets/images/currency/crypto-img5.png"
  
  export default {
    setup() {
      const coins = ref([
        {
          name: "Bitcoin",
          symbol: "BTC",
          price: "$45,138",
          change: "+ 27%",
          changeClass: "text-success-main text-md",
          img: crypto1,
          bgClass: "bg-gradient-end-3",
          chartId: "bitcoinAreaChart",
          chartColor: "#F98C08",
        },
        {
          name: "Ethereum",
          symbol: "ETH",
          price: "$45,138",
          change: "- 27%",
          changeClass: "text-danger-main text-md",
          img: crypto2,
          bgClass: "bg-gradient-end-1",
          chartId: "ethereumAreaChart",
          chartColor: "#5F80FF",
        },
        {
          name: "Solana",
          symbol: "SOL",
          price: "$45,138",
          change: "+ 27%",
          changeClass: "text-success-main text-md",
          img: crypto3,
          bgClass: "bg-gradient-end-5",
          chartId: "solanaAreaChart",
          chartColor: "#C817F8",
        },
        {
          name: "Litecoin",
          symbol: "LTE",
          price: "$45,138",
          change: "+ 27%",
          changeClass: "text-success-main text-md",
          img: crypto4,
          bgClass: "bg-gradient-end-6",
          chartId: "litecoinAreaChart",
          chartColor: "#2171EA",
        },
        {
          name: "Dogecoin",
          symbol: "DOGE",
          price: "$45,138",
          change: "+ 27%",
          changeClass: "text-success-main text-md",
          img: crypto5,
          bgClass: "bg-gradient-end-3",
          chartId: "dogecoinAreaChart",
          chartColor: "#C2A633",
        },
      ]);
  
      const createCoinChart = (chartId, chartColor) => {
        let currentYear = new Date().getFullYear();
  
        var options = {
          series: [
            {
              name: 'series1',
              data: [31, 24, 30, 25, 32, 28, 40, 32, 42, 38, 40, 32, 38, 35, 45],
            },
          ],
          chart: {
            type: 'area',
            width: 150,
            height: 70,
            sparkline: {
              enabled: true,
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
            events: {
              mounted: function (chartContext, config) {
                document.querySelectorAll(`#${chartId} .apexcharts-marker`).forEach(marker => {
                  marker.style.filter = 'blur(2px)';
                });
              },
              updated: function (chartContext, config) {
                document.querySelectorAll(`#${chartId} .apexcharts-marker`).forEach(marker => {
                  marker.style.filter = 'blur(3px)';
                });
              },
            },
          },
          dataLabels: {
            enabled: false,
          },
          stroke: {
            curve: 'smooth',
            width: 2,
            colors: [chartColor],
            lineCap: 'round',
          },
          grid: {
            show: true,
            borderColor: 'transparent',
            strokeDashArray: 0,
            position: 'back',
            xaxis: {
              lines: {
                show: false,
              },
            },
            yaxis: {
              lines: {
                show: false,
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
              top: -3,
              right: 0,
              bottom: 0,
              left: 0,
            },
          },
          fill: {
            type: 'gradient',
            colors: [chartColor],
            gradient: {
              shade: 'light',
              type: 'vertical',
              shadeIntensity: 0.5,
              gradientToColors: [`${chartColor}00`],
              inverseColors: false,
              opacityFrom: 0.7,
              opacityTo: 0.3,
              stops: [0, 100],
            },
          },
          markers: {
            colors: [chartColor],
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
            categories: [`Jan ${currentYear}`, `Feb ${currentYear}`, `Mar ${currentYear}`, `Apr ${currentYear}`, `May ${currentYear}`, `Jun ${currentYear}`, `Jul ${currentYear}`, `Aug ${currentYear}`, `Sep ${currentYear}`, `Oct ${currentYear}`, `Nov ${currentYear}`, `Dec ${currentYear}`],
            tooltip: {
              enabled: false,
            },
          },
          yaxis: {
            labels: {
              show: false,
            },
          },
          tooltip: {
            x: {
              format: 'dd/MM/yy HH:mm',
            },
          },
        };
  
        var chart = new ApexCharts(document.querySelector(`#${chartId}`), options);
        chart.render();
      };
  
      onMounted(() => {
        // Create charts for all coins after component is mounted
        coins.value.forEach(coin => {
          createCoinChart(coin.chartId, coin.chartColor);
        });
      });
  
      return {
        coins,
      };
    },
  };
  </script>