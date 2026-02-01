<template>
    <div class="col-md-6">
      <div class="card radius-16">
        <div class="card-header">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
            <h6 class="mb-2 fw-bold text-lg mb-0">Monthly Expense Breakdown</h6>
          </div>
        </div>
        <div class="card-body">
          <div class="mb-3 d-flex">
            <svg xmlns="http://www.w3.org/2000/svg" width="464" height="12" viewBox="0 0 464 12" fill="none">
              <g clip-path="url(#clip0_6886_52892)">
                <rect width="464" height="12" rx="6" fill="#6B7280"/>
                <rect width="464" height="12" rx="6" fill="#06B6D4"/>
                <rect width="418" height="12" rx="6" fill="#22C55E"/>
                <rect width="365" height="12" rx="6" fill="#84CC16"/>
                <rect width="295" height="12" rx="6" fill="#EAB308"/>
                <rect width="210" height="12" rx="6" fill="#F59E0B"/>
                <rect width="111" height="12" rx="6" fill="#F97316"/>
              </g>
              <defs>
                <clipPath id="clip0_6886_52892">
                  <rect width="464" height="12" rx="6" fill="white"/>
                </clipPath>
              </defs>
            </svg>
          </div>
          <div v-for="(expense, index) in expenses" :key="index" :class="['d-flex align-items-center justify-content-between p-12', expense.bgClass]">
            <div class="d-flex align-items-center gap-2">
              <span :class="['w-12-px h-8-px', expense.iconClass, 'rounded-pill']"></span>
              <span class="text-secondary-light">{{ expense.name }}</span>
            </div>
            <div class="d-flex align-items-center gap-2">
              <span class="text-secondary-light">${{ expense.amount }}</span>
              <span class="text-primary-light fw-semibold">{{ expense.percentage }}%</span>
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
        expenses: [
          {
            name: 'Healthcare',
            amount: 1500,
            percentage: 40,
            iconClass: 'bg-orange',
            bgClass: 'bg-neutral-100'
          },
          {
            name: 'Education',
            amount: 1500,
            percentage: 40,
            iconClass: 'bg-warning-600',
            bgClass: 'bg-base'
          },
          {
            name: 'Clothes',
            amount: 1500,
            percentage: 40,
            iconClass: 'bg-warning-600',
            bgClass: 'bg-neutral-100'
          },
          {
            name: 'Food',
            amount: 1500,
            percentage: 30,
            iconClass: 'bg-success-600',
            bgClass: 'bg-base'
          },
          {
            name: 'Transport',
            amount: 1500,
            percentage: 20,
            iconClass: 'bg-success-600',
            bgClass: 'bg-neutral-100'
          },
          {
            name: 'Pets',
            amount: 1500,
            percentage: 20,
            iconClass: 'bg-cyan-600',
            bgClass: 'bg-base'
          }
        ]
      }
    }
  }
  </script>