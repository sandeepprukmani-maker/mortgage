<template>
    <div class="card h-100 p-0 radius-12">
        <div class="card-body p-24">
            <div class="d-flex flex-wrap align-items-center justify-content-between mb-36">
                <div>
                    <span class="text-secondary-light fw-medium text-sm mb-4">PORTFOLIO VALUE</span>
                    <div class="d-flex align-items-center gap-8">
                        <h4 class="text-lg mb-0">$5,260</h4>
                        <span class="bg-success-focus text-success-600 px-16 py-6 rounded-pill fw-semibold text-xs">
                            <i class="ri-arrow-up-s-fill"></i>
                            1.37%
                        </span>
                    </div>
                </div>
                <div class="d-flex align-items-center gap-16">
                    <select class="form-select bg-base form-select-sm w-auto radius-8">
                        <option>All coins</option>
                        <option>Bitcoin</option>
                        <option>Litecoin</option>
                        <option>Dogecoin</option>
                    </select>
                    <select class="form-select bg-base form-select-sm w-auto radius-8">
                        <option>Yearly</option>
                        <option>Monthly</option>
                        <option>Weekly</option>
                        <option>Today</option>
                    </select>
                </div>
            </div>

            <apexchart type="area" height="350" :options="chartOptions" :series="series"></apexchart>

            <h6 class="text-xl mb-16">Your Assets</h6>
            <div class="table-responsive scroll-sm">
                <table class="table bordered-table sm-table mb-0">
                    <thead>
                        <tr>
                            <th scope="col">
                                <div class="d-flex align-items-center gap-10">
                                    <div class="form-check style-check d-flex align-items-center">
                                        <input class="form-check-input radius-4 border input-form-dark" type="checkbox"
                                            id="selectAll" @change="toggleSelectAll" />
                                    </div>
                                    S.L
                                </div>
                            </th>
                            <th>Aset</th>
                            <th>Your Assets</th>
                            <th>Price</th>
                            <th>Change %</th>
                            <th>Allocation</th>
                            <th class="text-center">Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(asset, index) in paginatedAssets" :key="index">
                            <td>
                                <div class="d-flex align-items-center gap-10">
                                    <div class="form-check style-check d-flex align-items-center">
                                        <input class="form-check-input radius-4 border border-neutral-400"
                                            type="checkbox" v-model="asset.selected" />
                                    </div>
                                    {{ asset.id }}
                                </div>
                            </td>
                            <td>
                                <router-link to="marketplace-details" class="d-flex align-items-center">
                                    <img :src="asset.img" alt=""
                                        class="w-40-px h-40-px rounded-circle flex-shrink-0 me-12 overflow-hidden" />
                                    <span class="flex-grow-1 d-flex flex-column">
                                        <span class="text-md mb-0 fw-medium text-primary-light d-block">{{ asset.name
                                        }}</span>
                                        <span class="text-xs mb-0 fw-normal text-secondary-light">{{ asset.symbol
                                        }}</span>
                                    </span>
                                </router-link>
                            </td>
                            <td>{{ asset.amount }}</td>
                            <td>{{ asset.price }}</td>
                            <td>
                                <span
                                    :class="asset.change > 0 ? 'bg-success-focus text-success-600' : 'bg-danger-focus text-danger-600'"
                                    class="px-16 py-6 rounded-pill fw-semibold text-xs">
                                    <i :class="asset.change > 0 ? 'ri-arrow-up-s-fill' : 'ri-arrow-down-s-fill'"></i>
                                    {{ asset.change }}%
                                </span>
                            </td>
                            <td>
                                <div class="progress w-100 bg-primary-50 rounded-pill h-8-px">
                                    <div class="progress-bar bg-primary-600 rounded-pill"
                                        :style="{ width: asset.allocation + '%' }"></div>
                                </div>
                            </td>
                            <td class="text-center">
                                <span class="py-4 px-16 text-primary-600 bg-primary-50 radius-4">Buy / Sell</span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Pagination -->
            <Pagination
                :currentPage="currentPage"
                :totalPages="totalPages"
                :startIndex="startIndex"
                :endIndex="endIndex"
                :totalItems="assets.length"
                @page-changed="changePage"
            />
        </div>
    </div>
</template>

<script>
import VueApexCharts from 'vue3-apexcharts';
import Pagination from '@/components/pagination/index.vue'

import crypto1 from '@/assets/images/crypto/crypto-img1.png'
import crypto2 from '@/assets/images/crypto/crypto-img2.png'
import crypto3 from '@/assets/images/crypto/crypto-img3.png'
import crypto4 from '@/assets/images/crypto/crypto-img4.png'
import crypto5 from '@/assets/images/crypto/crypto-img5.png'
import crypto6 from '@/assets/images/crypto/crypto-img6.png'

export default {
    components: {
        apexchart: VueApexCharts,
        Pagination
    },
    data() {
        return {
            series: [
                {
                    name: 'Bitcoin',
                    data: [
                        [1327359600000, 30.95],
                        [1327446000000, 31.34],
                        [1327532400000, 31.18],
                        [1327618800000, 31.05],
                        [1327878000000, 31.00],
                        [1327964400000, 30.95],
                        [1328050800000, 31.24],
                        [1328137200000, 31.29],
                        [1328223600000, 31.85],
                        [1328482800000, 31.86],
                        [1328569200000, 32.28],
                        [1328655600000, 32.10],
                        [1328742000000, 32.65],
                        [1328828400000, 32.21],
                        [1329087600000, 32.35],
                        [1329174000000, 32.44],
                        [1329260400000, 32.46],
                        [1329346800000, 32.86],
                        [1329433200000, 32.75],
                        [1329778800000, 32.54],
                        [1329865200000, 32.33],
                        [1329951600000, 32.97],
                        [1330038000000, 33.41],
                        [1330297200000, 33.27],
                        [1330383600000, 33.27],
                        [1330470000000, 32.89],
                        [1330556400000, 33.10],
                        [1330642800000, 33.73],
                    ]
                }
            ],
            chartOptions: {
                chart: {
                    type: 'area',
                    stacked: false,
                    height: 350,
                    zoom: {
                        type: 'x',
                        enabled: true,
                        autoScaleYaxis: true
                    },
                    toolbar: {
                        show: false
                    }
                },
                stroke: {
                    curve: 'straight',
                    width: 2,
                    lineCap: 'round'
                },
                dataLabels: {
                    enabled: false
                },
                markers: {
                    size: 0
                },
                grid: {
                    borderColor: '#D1D5DB',
                    strokeDashArray: 3
                },
                fill: {
                    type: 'gradient',
                    gradient: {
                        type: 'vertical',
                        shadeIntensity: 1,
                        gradientToColors: ['#487FFF'],
                        inverseColors: false,
                        opacityFrom: 0.4,
                        opacityTo: 0.1,
                        stops: [0, 100]
                    }
                },
                yaxis: {
                    tickAmount: 4,
                    labels: {
                        formatter: function (val) {
                            return (val / 1000000).toFixed(0);
                        }
                    },
                    title: {
                        text: 'Price'
                    }
                },
                xaxis: {
                    type: 'datetime'
                },
                tooltip: {
                    shared: false,
                    y: {
                        formatter: function (val) {
                            return (val / 1000000).toFixed(0);
                        }
                    }
                }
            },
            assets: [
                { id: '01', name: 'Bitcoin', symbol: 'BTC', img: crypto1, amount: '0.3464 BTC', price: '$2,753.00', change: 1.37, allocation: 50, selected: false },
                { id: '02', name: 'Ethereum', symbol: 'ETH', img: crypto2, amount: '1.2345 ETH', price: '$2,753.00', change: 2.5, allocation: 80, selected: false },
                { id: '03', name: 'Litecoin', symbol: 'LTC', img: crypto3, amount: '10.456 LTC', price: '$2,753.00', change: -1.2, allocation: 40, selected: false },
                { id: '04', name: 'Dogecoin', symbol: 'DOGE', img: crypto4, amount: '2000 DOGE', price: '$2,753.00', change: 5.0, allocation: 80, selected: false },
                { id: '05', name: 'Polygon', symbol: 'MATIC', img: crypto6, amount: '50 MATIC', price: '$2,753.00', change: 10.0, allocation: 40, selected: false },
                { id: '06', name: 'Cardano', symbol: 'ADA', img: crypto5, amount: '1500 ADA', price: '$2,753.00', change: -2.0, allocation: 65, selected: false },
                { id: '07', name: 'Ripple', symbol: 'XRP', img: crypto5, amount: '1000 XRP', price: '$2,753.00', change: -3.0, allocation: 15, selected: false },
                { id: '08', name: 'Solana', symbol: 'SOL', img: crypto5, amount: '200 SOL', price: '$2,753.00', change: -1.0, allocation: 70, selected: false },
                { id: '09', name: 'Polkadot', symbol: 'DOT', img: crypto5, amount: '300 DOT', price: '$2,753.00', change: 0.5, allocation: 60, selected: false },
                { id: '10', name: 'Avalanche', symbol: 'AVAX', img: crypto5, amount: '100 AVAX', price: '$2,753.00', change: -1.0, allocation: 20, selected: false },
                { id: '11', name: 'Chainlink', symbol: 'LINK', img: crypto5, amount: '200 LINK', price: '$2,753.00', change: 0.0, allocation: 50, selected: false },
                { id: '12', name: 'Litecoin', symbol: 'LTC', img: crypto5, amount: '300 LTC', price: '$2,753.00', change: -2.0, allocation: 50, selected: false },
            ],
            currentPage: 1,
            perPage: 10
        };
    },
    computed: {
        totalPages() {
            return Math.ceil(this.assets.length / this.perPage);
        },
        startIndex() {
            return (this.currentPage - 1) * this.perPage;
        },
        endIndex() {
            return Math.min(this.startIndex + this.perPage, this.assets.length);
        },
        paginatedAssets() {
            return this.assets.slice(this.startIndex, this.endIndex);
        }
    },
    methods: {
        changePage(page) {
            if (page > 0 && page <= this.totalPages) {
                this.currentPage = page;
            }
        },
        toggleSelectAll(event) {
            const selectAllChecked = event.target.checked;
            this.assets.forEach(asset => {
                asset.selected = selectAllChecked;
            });
        }
    }
};
</script>
