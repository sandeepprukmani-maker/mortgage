<template>
    <div class="col-12">
      <div class="card radius-12">
        <div class="card-body p-16">
          <div class="row gy-4">
            <div class="col-xxl-3 col-xl-4 col-sm-6" v-for="(card, index) in cards" :key="index">
              <div
                class="px-20 py-16 shadow-none radius-8 h-100 left-line position-relative overflow-hidden"
                :class="[card.gradient, card.lineBg]"
              >
                <div class="d-flex flex-wrap align-items-center justify-content-between gap-1 mb-8">
                  <div>
                    <span class="mb-2 fw-medium text-secondary-light text-md">{{ card.title }}</span>
                    <h6 class="fw-semibold mb-1">{{ card.amount }}</h6>
                  </div>
                  <span
                    class="w-44-px h-44-px radius-8 d-inline-flex justify-content-center align-items-center text-2xl mb-12"
                    :class="[card.iconBg, card.iconColor]"
                  >
                    <i :class="card.icon"></i>
                  </span>
                </div>
                <p class="text-sm mb-0">
                  <span
                    class="px-1 rounded-2 fw-medium text-sm"
                    :class="[card.trendBg, card.trendColor]"
                  >
                    <i :class="card.trendIcon"></i> {{ card.trendPercent }}
                  </span>
                  From last month
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'StatsCards',
    data() {
      return {
        cards: [
          {
            title: 'Gross Sales',
            amount: '$40,000',
            icon: 'ri-shopping-cart-fill',
            iconBg: 'bg-primary-100',
            iconColor: 'text-primary-600',
            trendPercent: '80%',
            trendIcon: 'ri-arrow-right-up-line',
            trendBg: 'bg-success-focus',
            trendColor: 'text-success-main',
            gradient: 'gradient-deep-1',
            lineBg: 'line-bg-primary',
          },
          {
            title: 'Total Purchase',
            amount: '$35,000',
            icon: 'ri-handbag-fill',
            iconBg: 'bg-lilac-200',
            iconColor: 'text-lilac-600',
            trendPercent: '95%',
            trendIcon: 'ri-arrow-right-up-line',
            trendBg: 'bg-success-focus',
            trendColor: 'text-success-main',
            gradient: 'gradient-deep-2',
            lineBg: 'line-bg-lilac',
          },
          {
            title: 'Total Income',
            amount: '$30,000',
            icon: 'ri-shopping-cart-fill',
            iconBg: 'bg-success-200',
            iconColor: 'text-success-600',
            trendPercent: '30%',
            trendIcon: 'ri-arrow-right-down-line',
            trendBg: 'bg-danger-focus',
            trendColor: 'text-danger-main',
            gradient: 'gradient-deep-3',
            lineBg: 'line-bg-success',
          },
          {
            title: 'Total Expense',
            amount: '$7,000',
            icon: 'ri-shopping-cart-fill',
            iconBg: 'bg-warning-focus',
            iconColor: 'text-warning-600',
            trendPercent: '60%',
            trendIcon: 'ri-arrow-right-up-line',
            trendBg: 'bg-success-focus',
            trendColor: 'text-success-main',
            gradient: 'gradient-deep-4',
            lineBg: 'line-bg-warning',
          },
        ],
      };
    },
  };
  </script>
  