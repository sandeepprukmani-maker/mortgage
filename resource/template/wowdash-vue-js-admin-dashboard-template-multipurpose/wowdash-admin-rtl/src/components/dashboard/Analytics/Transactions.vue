<template>
    <div class="col-xxl-4">
      <div class="card h-100">
        <div class="card-body p-24">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
            <h6 class="mb-2 fw-bold text-lg">Transactions</h6>
            <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
              View All
              <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
            </a>
          </div>
  
          <div class="mt-32">
            <div
              v-for="(transaction, index) in transactions"
              :key="index"
              class="d-flex align-items-center justify-content-between gap-3 mb-24"
              :class="{'mb-0': index === transactions.length - 1}"
            >
              <div class="d-flex align-items-center gap-3">
                <div
                  class="w-40-px h-40-px rounded-circle d-flex justify-content-center align-items-center flex-shrink-0"
                  :class="transaction.bgClass"
                >
                  <img :src="transaction.icon" alt="" />
                </div>
                <div class="flex-grow-1">
                  <h6 class="text-md mb-0 fw-normal">{{ transaction.title }}</h6>
                  <span class="text-sm text-secondary-light fw-normal">{{ transaction.subtitle }}</span>
                </div>
              </div>
              <span class="text-secondary-light text-md fw-medium">{{ transaction.amount }}</span>
            </div>
          </div>
  
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import payment1 from '@/assets/images/home-nine/payment1.png'
  import payment2 from '@/assets/images/home-nine/payment2.png'
  import payment3 from '@/assets/images/home-nine/payment3.png'
  import payment4 from '@/assets/images/home-nine/payment4.png'

  export default {
    name: 'Transactions',
    data() {
      return {
        transactions: [
          {
            title: 'Wallet',
            subtitle: 'Payment',
            amount: '+$6200',
            icon: payment1,
            bgClass: 'bg-success-200',
          },
          {
            title: 'PayPal',
            subtitle: 'Payment',
            amount: '+$6200',
            icon: payment2,
            bgClass: 'bg-info-200',
          },
          {
            title: 'Credit Card',
            subtitle: 'Bill Payment',
            amount: '-$6200',
            icon: payment3,
            bgClass: 'bg-warning-200',
          },
          {
            title: 'Bank',
            subtitle: 'Bill Payment',
            amount: '+$6200',
            icon: payment4,
            bgClass: 'bg-lilac-200',
          },
        ],
      };
    },
  };
  </script>