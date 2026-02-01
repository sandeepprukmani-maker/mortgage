<template>
    <div class="col-xxl-12 col-lg-6">
      <div class="card h-100">
        <div class="card-body p-24">
          <span class="mb-4 text-sm text-secondary-light">Total Balance</span>
          <h6 class="mb-4">{{ totalBalance }}</h6>
  
          <ul
            class="nav nav-pills pill-tab mb-24 mt-28 border input-form-light p-1 radius-8 bg-neutral-50"
            id="pills-tab"
            role="tablist"
          >
            <li class="nav-item w-50" role="presentation">
              <button
                class="nav-link px-12 py-10 text-md w-100 text-center radius-8"
                :class="{ active: activeTab === 'Buy' }"
                @click="setActiveTab('Buy')"
                type="button"
                role="tab"
                aria-controls="pills-Buy"
                aria-selected="true"
              >
                Buy
              </button>
            </li>
            <li class="nav-item w-50" role="presentation">
              <button
                class="nav-link px-12 py-10 text-md w-100 text-center radius-8"
                :class="{ active: activeTab === 'Sell' }"
                @click="setActiveTab('Sell')"
                type="button"
                role="tab"
                aria-controls="pills-Sell"
                aria-selected="false"
              >
                Sell
              </button>
            </li>
          </ul>
  
          <div class="tab-content" id="pills-tabContent">
            <div
              class="tab-pane fade"
              :class="{ show: activeTab === 'Buy', active: activeTab === 'Buy' }"
              id="pills-Buy"
              role="tabpanel"
              aria-labelledby="pills-Buy-tab"
              tabindex="0"
            >
              <div class="mb-20">
                <label for="estimatedValue" class="fw-semibold mb-8 text-primary-light">
                  Estimated Purchase Value
                </label>
                <div class="input-group input-group-lg border input-form-light radius-8">
                  <input
                    type="text"
                    class="form-control bg-base border-0 radius-8"
                    v-model="buy.estimatedValue"
                    id="estimatedValue"
                    placeholder="Estimated Value"
                  />
                  <div class="input-group-text bg-neutral-50 border-0 fw-normal text-md ps-1 pe-1">
                    <select
                      v-model="buy.selectedCurrency"
                      class="form-select form-select-sm w-auto bg-transparent fw-bolder border-0 text-secondary-light"
                    >
                      <option class="bg-base">BTC</option>
                      <option class="bg-base">LTC</option>
                      <option class="bg-base">ETC</option>
                    </select>
                  </div>
                </div>
              </div>
  
              <div class="mb-20">
                <label for="tradeValue" class="fw-semibold mb-8 text-primary-light">Trade Value</label>
                <div class="input-group input-group-lg border input-form-light radius-8">
                  <input
                    type="text"
                    class="form-control bg-base border-0 radius-8"
                    v-model="buy.tradeValue"
                    id="tradeValue"
                    placeholder="Trade Value"
                  />
                  <div class="input-group-text bg-neutral-50 border-0 fw-normal text-md ps-1 pe-1">
                    <select
                      v-model="buy.selectedTradeCurrency"
                      class="form-select form-select-sm w-auto bg-transparent fw-bolder border-0 text-secondary-light"
                    >
                      <option class="bg-base">USD</option>
                      <option class="bg-base">BTC</option>
                      <option class="bg-base">LTC</option>
                      <option class="bg-base">ETC</option>
                    </select>
                  </div>
                </div>
              </div>
  
              <div class="mb-20">
                <label class="fw-semibold mb-8 text-primary-light">Trade Value</label>
                <textarea
                  v-model="buy.address"
                  class="form-control bg-base h-80-px radius-8"
                  placeholder="Enter Address"
                ></textarea>
              </div>
  
              <div class="mb-24">
                <span class="mb-4 text-sm text-secondary-light">Total Balance</span>
                <h6 class="mb-4 fw-semibold text-xl text-warning-main">{{ totalBalance }}</h6>
              </div>
  
              <a href="" class="btn btn-primary text-sm btn-sm px-8 py-12 w-100 radius-8">Transfer Now</a>
            </div>
  
            <div
              class="tab-pane fade"
              :class="{ show: activeTab === 'Sell', active: activeTab === 'Sell' }"
              id="pills-Sell"
              role="tabpanel"
              aria-labelledby="pills-Sell-tab"
              tabindex="0"
            >
              <div class="mb-20">
                <label for="estimatedValueSell" class="fw-semibold mb-8 text-primary-light">Estimated Purchase Value</label>
                <div class="input-group input-group-lg border input-form-light radius-8">
                  <input
                    type="text"
                    class="form-control border-0 radius-8"
                    v-model="sell.estimatedValue"
                    id="estimatedValueSell"
                    placeholder="Estimated Value"
                  />
                  <div class="input-group-text bg-neutral-50 border-0 fw-normal text-md ps-1 pe-1">
                    <select
                      v-model="sell.selectedCurrency"
                      class="form-select form-select-sm w-auto bg-transparent fw-bolder border-0 text-secondary-light"
                    >
                      <option>BTC</option>
                      <option>LTC</option>
                      <option>USD</option>
                      <option>ETC</option>
                    </select>
                  </div>
                </div>
              </div>
  
              <div class="mb-20">
                <label for="tradeValueSell" class="fw-semibold mb-8 text-primary-light">Trade Value</label>
                <div class="input-group input-group-lg border input-form-light radius-8">
                  <input
                    type="text"
                    class="form-control border-0 radius-8"
                    v-model="sell.tradeValue"
                    id="tradeValueSell"
                    placeholder="Trade Value"
                  />
                  <div class="input-group-text bg-neutral-50 border-0 fw-normal text-md ps-1 pe-1">
                    <select
                      v-model="sell.selectedTradeCurrency"
                      class="form-select form-select-sm w-auto bg-transparent fw-bolder border-0 text-secondary-light"
                    >
                      <option>BTC</option>
                      <option>LTC</option>
                      <option>USD</option>
                      <option>ETC</option>
                    </select>
                  </div>
                </div>
              </div>
  
              <div class="mb-20">
                <label class="fw-semibold mb-8">Trade Value</label>
                <textarea
                  v-model="sell.address"
                  class="form-control h-80-px radius-8"
                  placeholder="Enter Address"
                ></textarea>
              </div>
  
              <div class="mb-24">
                <span class="mb-4 text-sm text-secondary-light">Total Balance</span>
                <h6 class="mb-4 fw-semibold text-xl text-warning-main">{{ totalBalance }}</h6>
              </div>
  
              <a href="" class="btn btn-primary text-sm btn-sm px-8 py-12 w-100 radius-8">Transfer Now</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        totalBalance: '$320,320.00',
        activeTab: 'Buy', // Default active tab
        buy: {
          estimatedValue: '',
          selectedCurrency: 'BTC',
          tradeValue: '',
          selectedTradeCurrency: 'USD',
          address: '',
        },
        sell: {
          estimatedValue: '',
          selectedCurrency: 'BTC',
          tradeValue: '',
          selectedTradeCurrency: 'USD',
          address: '',
        },
      };
    },
    methods: {
      setActiveTab(tab) {
        this.activeTab = tab;
      },
    },
  };
  </script>