<template>
    <div class="col-lg-3">
      <div class="card h-100">
        <div class="card-body p-0">
          <div class="px-24 py-20">
            <span class="mb-8">WowDash</span>
            <h5 class="text-2xl">$40,570.85</h5>
            <div
              class="mt-24 pb-24 mb-24 border-bottom d-flex align-items-center gap-16 justify-content-between flex-wrap">
              <div class="text-center d-flex align-items-center flex-column" v-for="(action, index) in actions" :key="index">
                <span
                  class="w-60-px h-60-px bg-primary-50 text-primary-600 text-2xl d-inline-flex justify-content-center align-items-center rounded-circle">
                  <i :class="action.icon"></i>
                </span>
                <span class="text-primary-light fw-medium mt-6">{{ action.label }}</span>
              </div>
            </div>
  
            <div class="d-flex align-items-center justify-content-between gap-8 pb-24 border-bottom">
              <h6 class="text-lg mb-0">Watchlist</h6>
              <a href="#" class="text-primary-600 fw-medium text-md">Sell all</a>
            </div>
  
            <div
              class="d-flex align-items-center justify-content-between flex-wrap gap-8 py-16 border-bottom"
              v-for="(item, index) in watchlist"
              :key="index"
            >
              <div class="d-flex align-items-center">
                <img :src="item.img" alt="" class="w-40-px h-40-px rounded-circle flex-shrink-0 me-12 overflow-hidden" />
                <div class="flex-grow-1 d-flex flex-column">
                  <span class="text-md mb-0 fw-medium text-primary-light d-block">{{ item.name }}</span>
                  <span class="text-xs mb-0 fw-normal text-secondary-light">{{ item.symbol }}</span>
                </div>
              </div>
              <div class="d-flex flex-column">
                <span class="text-md mb-0 fw-medium text-primary-light d-block">{{ item.value }}</span>
                <span class="text-xs mb-0 fw-normal text-secondary-light">{{ item.amount }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import crypto1 from '@/assets/images/crypto/crypto-img1.png'
  import crypto2 from '@/assets/images/crypto/crypto-img2.png'
  import crypto5 from '@/assets/images/crypto/crypto-img5.png'
  import crypto6 from '@/assets/images/crypto/crypto-img6.png'
  
  const actions = [
    { icon: 'ri-add-line', label: 'Buy' },
    { icon: 'ri-arrow-left-right-line', label: 'Swap' },
    { icon: 'ri-upload-2-line', label: 'Send' },
    { icon: 'ri-download-2-line', label: 'Receive' }
  ]
  
  const watchlist = [
    {
      name: 'Bitcoin',
      symbol: 'BTC',
      value: '$1,236.21',
      amount: '1.4363 BTC',
      img: crypto1
    },
    {
      name: 'Ethereum',
      symbol: 'ETH',
      value: '$1,236.21',
      amount: '1.4363 ETH',
      img: crypto2
    },
    {
      name: 'Dogecoin',
      symbol: 'DOGE',
      value: '$1,658',
      amount: '1.4363 DOGE',
      img: crypto5
    },
    {
      name: 'Digibyte',
      symbol: 'DGB',
      value: '$165,8',
      amount: '1.4363 DGB',
      img: crypto6
    }
  ]
  </script>
  