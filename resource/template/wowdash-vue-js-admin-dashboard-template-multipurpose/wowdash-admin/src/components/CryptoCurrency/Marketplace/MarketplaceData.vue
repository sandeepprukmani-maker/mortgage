<template>
  <div class="card h-100 p-0 radius-12">
    <div class="card-header border-bottom bg-base py-16 px-24 d-flex align-items-center flex-wrap gap-3 justify-content-between">
      <div class="d-flex align-items-center flex-wrap gap-3">
        <span class="text-md fw-medium text-secondary-light mb-0">Show</span>
        <select v-model="coinsPerPage" @change="changePage(1)" class="form-select form-select-sm w-auto ps-12 py-6 radius-12 h-40-px">
          <option v-for="n in 10" :key="n" :value="n">{{ n }}</option>
        </select>
        <form class="navbar-search">
          <input type="text" class="bg-base h-40-px w-auto" name="search" placeholder="Search" />
          <iconify-icon icon="ion:search-outline" class="icon"></iconify-icon>
        </form>
        <button type="button" class="btn border py-8 text-secondary-light fw-medium bg-hover-neutral-50 radius-8">Watchlist</button>
      </div>
      <router-link to="/portfolio" class="btn btn-primary text-sm btn-sm px-24 py-10 radius-8">
        Portfolios
      </router-link>
    </div>

    <div class="card-body p-24">
      <div class="table-responsive scroll-sm">
        <table class="table bordered-table sm-table mb-0">
          <thead>
            <tr>
              <th scope="col">
                <div class="d-flex align-items-center gap-10">
                  <div class="form-check style-check d-flex align-items-center">
                    <input class="form-check-input radius-4 border input-form-dark" type="checkbox"
                      id="selectAll" v-model="selectAll" @change="toggleSelectAll" />
                  </div>
                  S.L
                </div>
              </th>
              <th scope="col">Asset</th>
              <th scope="col">Circulating Supply</th>
              <th scope="col">Price</th>
              <th scope="col">Market Cap</th>
              <th scope="col">Change %</th>
              <th scope="col">Last (24H)</th>
              <th scope="col" class="text-center">Watchlist</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(coin, index) in paginatedCoins" :key="coin.id">
              <td>
                <div class="d-flex align-items-center gap-10">
                  <div class="form-check style-check d-flex align-items-center">
                    <input class="form-check-input radius-4 border border-neutral-400"
                      type="checkbox" :id="coin.id" :value="coin.id" v-model="selectedCoins" />
                  </div>
                  {{ (startIndex + index + 1).toString().padStart(2, '0') }}
                </div>
              </td>
              <td>
                <router-link to="/marketplace-details" class="d-flex align-items-center">
                  <img :src="coin.img" alt=""
                    class="w-40-px h-40-px rounded-circle flex-shrink-0 me-12 overflow-hidden" />
                  <span class="flex-grow-1 d-flex flex-column">
                    <span class="text-md mb-0 fw-medium text-primary-light d-block">{{ coin.name }}</span>
                    <span class="text-xs mb-0 fw-normal text-secondary-light">{{ coin.symbol }}</span>
                  </span>
                </router-link>
              </td>
              <td>{{ coin.supply }}</td>
              <td>{{ coin.price }}</td>
              <td>{{ coin.marketCap }}</td>
              <td>
                <span
                  :class="['px-16 py-6 rounded-pill fw-semibold text-xs', coin.change > 0 ? 'bg-success-focus text-success-600' : 'bg-danger-focus text-danger-600']">
                  <i :class="coin.change > 0 ? 'ri-arrow-up-s-fill' : 'ri-arrow-down-s-fill'"></i>
                  {{ Math.abs(coin.change).toFixed(2) }}%
                </span>
              </td>
              <td><div :id="coin.chartId" class="remove-tooltip-title rounded-tooltip-value"></div></td>
              <td class="text-center">
                <button type="button"
                  class="star-btn text-2xl text-neutral-400 text-hover-primary-600 line-height-1"
                  @click="toggleStar(index)">
                  <i :class="coin.starred ? 'ri-star-fill text-primary-600' : 'ri-star-line'"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

    <!-- pagination -->
      <Pagination
        :currentPage="currentPage"
        :totalPages="totalPages"
        :startIndex="startIndex"
        :endIndex="endIndex"
        :totalItems="coins.length"
        @page-changed="changePage"
      />
    </div>
  </div>
</template>

<script>
import ApexCharts from 'apexcharts';
import Pagination from '@/components/pagination/index.vue';

import crypto1 from '@/assets/images/crypto/crypto-img1.png';
import crypto2 from '@/assets/images/crypto/crypto-img2.png';
import crypto3 from '@/assets/images/crypto/crypto-img3.png';
import crypto4 from '@/assets/images/crypto/crypto-img4.png';
import crypto5 from '@/assets/images/crypto/crypto-img5.png';
import crypto6 from '@/assets/images/crypto/crypto-img6.png';

export default {
  name: 'CryptoTable',
  components: { Pagination },
  data() {
    return {
      selectAll: false,
      selectedCoins: [],
      currentPage: 1,
      coinsPerPage: 10,
      charts: {},
      dates: [
        [1327359600000, 30.95], [1327446000000, 31.34], [1327532400000, 31.18], [1327618800000, 31.05],
        [1327878000000, 31.0], [1327964400000, 30.95], [1328050800000, 31.24], [1328137200000, 31.29],
        [1328223600000, 31.85], [1328482800000, 31.86], [1328569200000, 32.28], [1328655600000, 32.1],
        [1328742000000, 32.65], [1328828400000, 32.21], [1329087600000, 32.35], [1329174000000, 32.44],
        [1329260400000, 32.46], [1329346800000, 32.86], [1329433200000, 32.75], [1329778800000, 32.54]
      ],
      coins: [
        { id: '01', name: 'Bitcoin', symbol: 'BTC', supply: '0.3464 BTC', price: '$2,753.00', marketCap: '$361.32B', change: 1.37, chartId: 'chart1', img: crypto1, starred: false },
        { id: '02', name: 'Ethereum', symbol: 'ETH', supply: '0.5464 ETH', price: '$1,800.00', marketCap: '$218.32B', change: 2.15, chartId: 'chart2', img: crypto2, starred: false },
        { id: '03', name: 'Litecoin', symbol: 'LTC', supply: '0.5464 LTC', price: '$185.00', marketCap: '$12.00B', change: -0.87, chartId: 'chart3', img: crypto3, starred: false },
        { id: '04', name: 'Binance', symbol: 'BNB', supply: '0.5464 BNB', price: '$300.00', marketCap: '$50.00B', change: 0.67, chartId: 'chart4', img: crypto4, starred: false },
        { id: '05', name: 'Dogecoin', symbol: 'DOGE', supply: '0.5464 DOGE', price: '$0.07', marketCap: '$10.00B', change: -1.37, chartId: 'chart5', img: crypto6, starred: false },
        { id: '06', name: 'Polygon', symbol: 'MATIC', supply: '0.5464 MATIC', price: '$0.89', marketCap: '$7.00B', change: 0.45, chartId: 'chart6', img: crypto5, starred: false },
        { id: '07', name: 'Polygon', symbol: 'MATIC', supply: '0.5464 MATIC', price: '$0.89', marketCap: '$7.00B', change: -0.45, chartId: 'chart7', img: crypto5, starred: false },
        { id: '08', name: 'Polygon', symbol: 'MATIC', supply: '0.5464 MATIC', price: '$0.89', marketCap: '$7.00B', change: -0.45, chartId: 'chart8', img: crypto5, starred: false },
        { id: '09', name: 'Polygon', symbol: 'MATIC', supply: '0.5464 MATIC', price: '$0.89', marketCap: '$7.00B', change: -0.45, chartId: 'chart9', img: crypto5, starred: false },
        { id: '10', name: 'Polygon', symbol: 'MATIC', supply: '0.5464 MATIC', price: '$0.89', marketCap: '$7.00B', change: -0.45, chartId: 'chart10', img: crypto5, starred: false },
      ]
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.coins.length / this.coinsPerPage);
    },
    startIndex() {
      return (this.currentPage - 1) * this.coinsPerPage;
    },
    endIndex() {
      return this.startIndex + this.paginatedCoins.length;
    },
    paginatedCoins() {
      return this.coins.slice(this.startIndex, this.startIndex + this.coinsPerPage);
    },
  },
  mounted() {
    this.coins.forEach((coin) => {
      this.renderChart(coin.chartId, coin.change > 0 ? '#45B369' : '#EF4A00', coin.name);
    });
  },
  watch: {
    selectedCoins(newVal) {
      this.selectAll = newVal.length === this.coins.length;
    },
  },
  methods: {
    toggleSelectAll() {
      this.selectedCoins = this.selectAll ? this.coins.map(c => c.id) : [];
    },
    toggleStar(index) {
      this.coins[index].starred = !this.coins[index].starred;
    },
    changePage(page) {
      if (page < 1 || page > this.totalPages) return;
      this.currentPage = page;
    },
    renderChart(containerId, color, coinName) {
      if (this.charts[containerId]) {
        this.charts[containerId].destroy();
      }

      const options = {
        series: [{ name: coinName, data: this.dates }],
        chart: {
          type: 'area',
          stacked: false,
          width: 76,
          height: 40,
          sparkline: { enabled: true },
          toolbar: { show: false },
        },
        stroke: { curve: 'straight', width: 2, colors: [color] },
        dataLabels: { enabled: false },
        markers: { size: 0 },
        fill: {
          type: 'gradient',
          gradient: {
            type: 'vertical',
            shadeIntensity: 1,
            gradientToColors: [color],
            opacityFrom: 0.4,
            opacityTo: 0.1,
            stops: [0, 100],
          },
        },
        yaxis: { labels: { show: false } },
        xaxis: { type: 'datetime', labels: { show: false } },
        tooltip: { enabled: false },
      };

      const chart = new ApexCharts(document.querySelector(`#${containerId}`), options);
      chart.render();
      this.charts[containerId] = chart;
    }
  }
};
</script>
