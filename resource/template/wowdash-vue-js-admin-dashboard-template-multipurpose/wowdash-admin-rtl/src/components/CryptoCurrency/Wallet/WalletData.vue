<template>
    <div class="col-lg-9">
        <div class="card h-100 p-0 radius-12">
            <div
                class="card-header border-bottom bg-base py-16 px-24 d-flex align-items-center flex-wrap gap-3 justify-content-between">
                <div class="d-flex align-items-center flex-wrap gap-3">
                    <span class="text-md fw-medium text-secondary-light mb-0">Show</span>
                    <select class="form-select form-select-sm w-auto ps-12 py-6 radius-12 h-40-px" v-model="showCount">
                        <option v-for="i in 10" :key="i">{{ i }}</option>
                    </select>
                    <form class="navbar-search" @submit.prevent>
                        <input type="text" class="bg-base h-40-px w-auto" name="search" placeholder="Search"
                            v-model="search">
                        <iconify-icon icon="ion:search-outline" class="icon"></iconify-icon>
                    </form>
                    <select class="form-select form-select-sm w-auto ps-12 py-6 radius-12 h-40-px" v-model="status">
                        <option>Status</option>
                        <option>Active</option>
                        <option>Inactive</option>
                    </select>
                </div>
                <button type="button"
                    class="btn btn-primary text-sm btn-sm px-12 py-12 radius-8 d-flex align-items-center gap-2"
                    data-bs-toggle="modal" data-bs-target="#exampleModalEdit">
                    <iconify-icon icon="ic:baseline-plus" class="icon text-xl line-height-1"></iconify-icon>
                    Connect Wallet
                </button>
            </div>

            <div class="card-body p-24">
                <div class="table-responsive scroll-sm">
                    <table class="table bordered-table sm-table mb-0">
                        <thead>
                            <tr>
                                <th scope="col">
                                    <div class="d-flex align-items-center gap-10">
                                        <div class="form-check style-check d-flex align-items-center">
                                            <input class="form-check-input radius-4 border input-form-dark"
                                                type="checkbox" id="selectAll" v-model="selectAll" @change="toggleAll">
                                        </div>
                                        S.L
                                    </div>
                                </th>
                                <th scope="col">Aset</th>
                                <th scope="col">Amount</th>
                                <th scope="col">Price</th>
                                <th scope="col">Change %</th>
                                <th scope="col">Allocation</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(asset, index) in paginatedAssets" :key="index">
                                <td>
                                    <div class="d-flex align-items-center gap-10">
                                        <div class="form-check style-check d-flex align-items-center">
                                            <input class="form-check-input radius-4 border border-neutral-400"
                                                type="checkbox" v-model="asset.selected">
                                        </div>
                                        {{ startIndex + index + 1 < 10 ? '0' + (startIndex + index + 1) : startIndex +
                                            index + 1 }} </div>
                                </td>
                                <td>
                                    <router-link to="/marketplace-details" class="d-flex align-items-center">
                                        <img :src="asset.img" alt=""
                                            class="w-40-px h-40-px rounded-circle flex-shrink-0 me-12 overflow-hidden">
                                        <span class="flex-grow-1 d-flex flex-column">
                                            <span class="text-md mb-0 fw-medium text-primary-light d-block">{{
                                                asset.name }}</span>
                                            <span class="text-xs mb-0 fw-normal text-secondary-light">{{ asset.symbol
                                                }}</span>
                                        </span>
                                    </router-link>
                                </td>
                                <td>{{ asset.amount }}</td>
                                <td>{{ asset.price }}</td>
                                <td>
                                    <span :class="[
                                        asset.change.startsWith('-') ? 'bg-danger-focus text-danger-600' : 'bg-success-focus text-success-600',
                                        'px-16 py-6 rounded-pill fw-semibold text-xs'
                                    ]">
                                        <i
                                            :class="asset.change.startsWith('-') ? 'ri-arrow-down-s-fill' : 'ri-arrow-up-s-fill'"></i>
                                        {{ asset.change }}
                                    </span>
                                </td>
                                <td>
                                    <div class="progress w-100 bg-primary-50 rounded-pill h-8-px" role="progressbar"
                                        aria-valuemin="0" aria-valuemax="100" :aria-valuenow="asset.allocation">
                                        <div class="progress-bar bg-primary-600 rounded-pill"
                                            :style="{ width: asset.allocation + '%' }">
                                        </div>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Pagination -->
                <Pagination :currentPage="currentPage" :totalPages="totalPages" :startIndex="startIndex"
                    :endIndex="endIndex" :totalItems="assets.length" @page-changed="changePage" />

            </div>
        </div>
    </div>

    <!-- model -->
    <div class="modal fade" id="exampleModalEdit" tabindex="-1" aria-labelledby="exampleModalEditLabel"
        aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content radius-16 bg-base">
                <div class="modal-header py-16 px-24 border border-top-0 border-start-0 border-end-0">
                    <h1 class="modal-title fs-5" id="exampleModalEditLabel">Connect Wallet</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body p-24">
                    <div class="d-flex flex-column gap-8">
                        <a href="#"
                            class="d-flex align-items-center justify-content-between gap-8 p-16 border radius-8 bg-hover-neutral-50"
                            v-for="(wallet, index) in wallets" :key="index">
                            <span class="d-flex align-items-center gap-16">
                                <img :src="wallet.img" alt="" class="flex-shrink-0 me-12 overflow-hidden">
                                <span class="text-md mb-0 fw-medium text-primary-light d-block">{{ wallet.name }}</span>
                            </span>
                            <span class="text-secondary-light text-md"><i class="ri-arrow-right-s-line"></i></span>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<script setup>
import crypto1 from '@/assets/images/crypto/crypto-img1.png'
import crypto2 from '@/assets/images/crypto/crypto-img2.png'
import crypto3 from '@/assets/images/crypto/crypto-img3.png'
import crypto4 from '@/assets/images/crypto/crypto-img4.png'
import crypto5 from '@/assets/images/crypto/crypto-img5.png'
import crypto6 from '@/assets/images/crypto/crypto-img6.png'

import walletIcon1 from "@/assets/images/crypto/wallet-icon1.png"
import walletIcon2 from "@/assets/images/crypto/wallet-icon2.png"
import walletIcon3 from "@/assets/images/crypto/wallet-icon3.png"
import walletIcon4 from "@/assets/images/crypto/wallet-icon4.png"

import { ref, computed } from 'vue';
import Pagination from '@/components/pagination/index.vue'

const showCount = ref(10);
const search = ref('');
const status = ref('Status');
const selectAll = ref(false);
const currentPage = ref(1);

const assets = ref([
    {
        selected: false,
        img: crypto1,
        name: 'Bitcoin',
        symbol: 'BTC',
        amount: '0.3464 BTC',
        price: '$2,753.00',
        change: '1.37%',
        allocation: 50
    },
    {
        selected: false,
        img: crypto2,
        name: 'Ethereum',
        symbol: 'ETH',
        amount: '0.5464 ETH',
        price: '$2,753.00',
        change: '-1.37%',
        allocation: 80
    },
    {
        selected: false,
        img: crypto3,
        name: 'Litecoin',
        symbol: 'LTC',
        amount: '0.5464 LTC',
        price: '$2,753.00',
        change: '1.37%',
        allocation: 40
    },
    {
        selected: false,
        img: crypto4,
        name: 'Binance',
        symbol: 'BNB',
        amount: '0.5464 BNB',
        price: '$2,753.00',
        change: '-0.50%',
        allocation: 70
    },
    {
        selected: false,
        img: crypto6,
        name: 'Dogecoin',
        symbol: 'DOGE',
        amount: '0.5464 DOGE',
        price: '$2,753.00',
        change: '1.37%',
        allocation: 40
    },
    {
        selected: false,
        img: crypto5,
        name: 'Polygon',
        symbol: 'MATIC',
        amount: '0.5464 MATIC',
        price: '$2,753.00',
        change: '1.37%',
        allocation: 80
    },
    {
        selected: false,
        img: crypto5,
        name: 'Polygon',
        symbol: 'MATIC',
        amount: '0.5464 MATIC',
        price: '$2,753.00',
        change: '-1.37%',
        allocation: 80
    },
    {
        selected: false,
        img: crypto5,
        name: 'Polygon',
        symbol: 'MATIC',
        amount: '0.5464 MATIC',
        price: '$2,753.00',
        change: '-1.37%',
        allocation: 80
    },
    {
        selected: false,
        img: crypto5,
        name: 'Polygon',
        symbol: 'MATIC',
        amount: '0.5464 MATIC',
        price: '$2,753.00',
        change: '-1.37%',
        allocation: 80
    },
    {
        selected: false,
        img: crypto5,
        name: 'Polygon',
        symbol: 'MATIC',
        amount: '0.5464 MATIC',
        price: '$2,753.00',
        change: '-1.37%',
        allocation: 80
    },
    {
        selected: false,
        img: crypto5,
        name: 'Polygon',
        symbol: 'MATIC',
        amount: '0.5464 MATIC',
        price: '$2,753.00',
        change: '-1.37%',
        allocation: 80
    },
],
);

// Model data
const wallets = [
    { name: "Bitcoin", img: walletIcon1 },
    { name: "Coinbase Wallet", img: walletIcon2 },
    { name: "Exodus Wallet", img: walletIcon3 },
    { name: "Trust Wallet", img: walletIcon4 }
];

// Pagination logic
const totalPages = computed(() => Math.ceil(assets.value.length / showCount.value));
const startIndex = computed(() => (currentPage.value - 1) * showCount.value);
const endIndex = computed(() => Math.min(startIndex.value + showCount.value, assets.value.length));

const paginatedAssets = computed(() => {
    return assets.value.slice(startIndex.value, endIndex.value);
});

const changePage = (page) => {
    if (page > 0 && page <= totalPages.value) {
        currentPage.value = page;
    }
};

const toggleAll = () => {
    assets.value.forEach(asset => {
        asset.selected = selectAll.value;
    });
};
</script>
