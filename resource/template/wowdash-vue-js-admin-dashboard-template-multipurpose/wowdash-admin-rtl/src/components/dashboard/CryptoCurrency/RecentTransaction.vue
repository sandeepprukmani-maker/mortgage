<template>
    <div class="col-xxl-12">
      <div class="card h-100">
        <div class="card-body p-24">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between mb-20">
            <h6 class="mb-2 fw-bold text-lg mb-0">Recent Transaction</h6>
            <a href="javascript:void(0)"
               class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
              View All
              <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
            </a>
          </div>
          <div class="table-responsive scroll-sm">
            <table class="table bordered-table mb-0 xsm-table">
              <thead>
                <tr>
                  <th scope="col">Ast</th>
                  <th scope="col">Date & Time</th>
                  <th scope="col">Amount</th>
                  <th scope="col">Address</th>
                  <th scope="col" class="text-center">Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(transaction, index) in transactions" :key="index">
                  <td>
                    <div class="d-flex align-items-center gap-2">
                      <span :class="transaction.iconClass" class="w-32-px h-32-px d-flex align-items-center justify-content-center rounded-circle text-xl">
                        <iconify-icon :icon="transaction.icon" class="icon"></iconify-icon>
                      </span>
                      <span class="fw-medium">{{ transaction.asset }}</span>
                    </div>
                  </td>
                  <td>
                    <span class="text-primary-light d-block fw-medium">{{ transaction.time }}</span>
                    <span class="text-secondary-light text-sm">{{ transaction.date }}</span>
                  </td>
                  <td>
                    <span class="text-primary-light d-block fw-medium">{{ transaction.amount }}</span>
                    <span class="text-secondary-light text-sm">{{ transaction.amountInUSD }}</span>
                  </td>
                  <td>{{ transaction.address }}</td>
                  <td class="text-center">
                    <span :class="transaction.statusClass" class="px-16 py-4 radius-4 fw-medium text-sm">{{ transaction.status }}</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        transactions: [
          {
            asset: 'Bitcoin',
            time: '10:34 AM',
            date: '27 Mar 2024',
            amount: '+ 0.431 BTC',
            amountInUSD: '$3,480.90',
            address: 'Abc.........np562',
            status: 'Completed',
            iconClass: 'text-success-main bg-success-focus',
            icon: 'tabler:arrow-up-right',
            statusClass: 'bg-success-focus text-success-main'
          },
          {
            asset: 'Bitcoin',
            time: '10:34 AM',
            date: '27 Mar 2024',
            amount: '+ 0.431 BTC',
            amountInUSD: '$3,480.90',
            address: 'Abc.........np562',
            status: 'Terminated',
            iconClass: 'text-danger-main bg-danger-focus',
            icon: 'tabler:arrow-down-left',
            statusClass: 'bg-danger-focus text-danger-main'
          },
          {
            asset: 'Bitcoin',
            time: '10:34 AM',
            date: '27 Mar 2024',
            amount: '+ 0.431 BTC',
            amountInUSD: '$3,480.90',
            address: 'Abc.........np562',
            status: 'Completed',
            iconClass: 'text-success-main bg-success-focus',
            icon: 'tabler:arrow-up-right',
            statusClass: 'bg-success-focus text-success-main'
          },
          {
            asset: 'Bitcoin',
            time: '10:34 AM',
            date: '27 Mar 2024',
            amount: '+ 0.431 BTC',
            amountInUSD: '$3,480.90',
            address: 'Abc.........np562',
            status: 'Terminated',
            iconClass: 'text-danger-main bg-danger-focus',
            icon: 'tabler:arrow-down-left',
            statusClass: 'bg-danger-focus text-danger-main'
          },
          {
            asset: 'Bitcoin',
            time: '10:34 AM',
            date: '27 Mar 2024',
            amount: '+ 0.431 BTC',
            amountInUSD: '$3,480.90',
            address: 'Abc.........np562',
            status: 'Completed',
            iconClass: 'text-success-main bg-success-focus',
            icon: 'tabler:arrow-up-right',
            statusClass: 'bg-success-focus text-success-main'
          }
        ]
      };
    }
  };
  </script>