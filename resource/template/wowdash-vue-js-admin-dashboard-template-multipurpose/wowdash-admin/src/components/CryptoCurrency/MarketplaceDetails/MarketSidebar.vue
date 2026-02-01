<template>
    <div class="col-xxl-3 col-lg-4">
      <div class="card h-100">
        <div class="card-body p-0">
          <div class="p-24 border-bottom">
            <ul class="nav nav-pills style-three pill-tab border input-form-light p-0 radius-8 bg-neutral-50" role="tablist">
              <li class="nav-item" role="presentation">
                <button class="nav-link px-12 py-10 text-md w-100 text-center radius-8" :class="{ active: activeTab === 'Buy' }"
                  @click="activeTab = 'Buy'" type="button" role="tab">Buy</button>
              </li>
              <li class="nav-item" role="presentation">
                <button class="nav-link px-12 py-10 text-md w-100 text-center radius-8" :class="{ active: activeTab === 'Sell' }"
                  @click="activeTab = 'Sell'" type="button" role="tab">Sell</button>
              </li>
              <li class="nav-item" role="presentation">
                <button class="nav-link px-12 py-10 text-md w-100 text-center radius-8" :class="{ active: activeTab === 'Convert' }"
                  @click="activeTab = 'Convert'" type="button" role="tab">Convert</button>
              </li>
            </ul>
  
            <div class="tab-content">
              <div v-for="tab in ['Buy', 'Sell', 'Convert']" :key="tab"
                class="tab-pane fade"
                :class="{ 'show active': activeTab === tab }"
                role="tabpanel"
                tabindex="0">
                <div>
                  <div class="text-center mt-24">
                    <h3 class="text-neutral-400 mb-16">$0</h3>
                    <span class="text-neutral-500 text-sm">You can buy up to $25,000</span>
                  </div>
                  <div class="mt-24 border radius-8 position-relative">
                    <button type="button"
                      class="bg-primary-600 w-40-px h-40-px rounded-circle border border-3 border-primary-100 d-flex justify-content-center align-items-center text-white position-absolute top-50 translate-middle-y end-0 me-60">
                      <i class="ri-arrow-up-down-line"></i>
                    </button>
                    <div class="p-16 d-flex align-items-center border-bottom">
                      <span class="text-neutral-500 fw-medium w-76-px border-end">Buy</span>
                      <div class="d-flex align-items-center justify-content-between flex-grow-1 ps-16">
                        <div class="d-flex align-items-center gap-8">
                          <img src="@/assets/images/crypto/crypto-img1.png" alt=""
                            class="w-24-px h-24-px rounded-circle flex-shrink-0 overflow-hidden">
                          <div class="flex-grow-1 d-flex flex-column">
                            <span class="text-sm mb-0 fw-medium text-primary-light d-block">ITC</span>
                          </div>
                        </div>
                        <a href="" class="text-md text-neutral-500 text-hover-primary-600"><i class="ri-arrow-right-s-line"></i></a>
                      </div>
                    </div>
                    <div class="p-16 d-flex align-items-center">
                      <span class="text-neutral-500 fw-medium w-76-px border-end">Pay with</span>
                      <div class="d-flex align-items-center justify-content-between flex-grow-1 ps-16">
                        <div class="d-flex align-items-center gap-8">
                          <img src="@/assets/images/crypto/paypal.png" alt=""
                            class="w-24-px h-24-px rounded-circle flex-shrink-0 overflow-hidden">
                          <div class="flex-grow-1 d-flex flex-column">
                            <span class="text-sm mb-0 fw-medium text-primary-light d-block">Paypal</span>
                          </div>
                        </div>
                        <a href="" class="text-md text-neutral-500 text-hover-primary-600"><i class="ri-arrow-right-s-line"></i></a>
                      </div>
                    </div>
                  </div>
                  <button type="button" class="btn btn-primary text-sm btn-sm px-12 py-16 w-100 radius-8 mt-24 pb-8"
                    data-bs-toggle="modal" data-bs-target="#exampleModalEdit">
                    Buy
                  </button>
                </div>
              </div>
            </div>
          </div>
  
          <div class="px-24 py-20">
            <div class="d-flex align-items-center justify-content-between gap-8 pb-24 border-bottom">
              <h6 class="text-lg mb-0">Watchlist</h6>
              <a href="#" class="text-primary-600 fw-medium text-md">Sell all</a>
            </div>
  
            <div v-for="(item, index) in watchlist" :key="index"
              class="d-flex align-items-center justify-content-between flex-wrap gap-8 py-16 border-bottom">
              <div class="d-flex align-items-center">
                <img :src="item.image" alt="" class="w-40-px h-40-px rounded-circle flex-shrink-0 me-12 overflow-hidden">
                <div class="flex-grow-1 d-flex flex-column">
                  <span class="text-md mb-0 fw-medium text-primary-light d-block">{{ item.name }}</span>
                  <span class="text-xs mb-0 fw-normal text-secondary-light">{{ item.symbol }}</span>
                </div>
              </div>
              <div class="d-flex flex-column">
                <span class="text-md mb-0 fw-medium text-primary-light d-block">{{ item.price }}</span>
                <span class="text-xs mb-0 fw-normal text-secondary-light">{{ item.amount }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Modal -->
      <div class="modal fade" id="exampleModalEdit" tabindex="-1" aria-labelledby="exampleModalEditLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog modal-dialog-centered">
          <div class="modal-content radius-16 bg-base">
            <div class="modal-body px-32 py-56">
              <div class="text-center">
                <span class="w-100-px h-100-px bg-success-600 rounded-circle d-inline-flex justify-content-center align-items-center text-2xxl mb-32 text-white">
                  <i class="ri-check-line"></i>
                </span>
                <h5 class="mb-8 text-2xl">Your purchase was successful!</h5>
                <p class="text-neutral-500 mb-0">
                  <span class="text-primary-600">16.2665 ITC</span> will be available in your portfolio on 10-10-2022
                </p>
                <router-link to="/" class="btn btn-primary-600 mt-32 px-24">Back to Dashboard</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import crypto1 from '@/assets/images/crypto/crypto-img1.png'
  import crypto2 from '@/assets/images/crypto/crypto-img2.png'
  import crypto5 from '@/assets/images/crypto/crypto-img5.png'
  import crypto6 from '@/assets/images/crypto/crypto-img6.png'
  
  const activeTab = ref('Buy')
  
  const watchlist = [
    {
      name: 'Bitcoin',
      symbol: 'BTC',
      price: '$1,236.21',
      amount: '1.4363 BTC',
      image: crypto1,
    },
    {
      name: 'Ethereum',
      symbol: 'ETH',
      price: '$1,236.21',
      amount: '1.4363 ETH',
      image: crypto2,
    },
    {
      name: 'Dogecoin',
      symbol: 'DOGE',
      price: '$1,658',
      amount: '1.4363 DOGE',
      image: crypto5,
    },
    {
      name: 'Digibyte',
      symbol: 'DGB',
      price: '$165,8',
      amount: '1.4363 DGB',
      image: crypto6,
    },
  ]
  </script>
  