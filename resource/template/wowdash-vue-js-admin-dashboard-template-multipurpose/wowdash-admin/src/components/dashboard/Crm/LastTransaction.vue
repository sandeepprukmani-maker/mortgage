<template>
    <div class="col-xxl-6">
      <div class="card h-100">
        <div class="card-header border-bottom bg-base py-16 px-24 d-flex align-items-center justify-content-between">
          <h6 class="text-lg fw-semibold mb-0">Last Transaction</h6>
          <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
            View All
            <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
          </a>
        </div>
        <div class="card-body p-24">
          <div class="table-responsive scroll-sm">
            <table class="table bordered-table mb-0">
              <thead>
                <tr>
                  <th scope="col">Transaction ID</th>
                  <th scope="col">Date</th>
                  <th scope="col">Status</th>
                  <th scope="col">Amount</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(transaction, index) in transactions" :key="index">
                  <td>{{ transaction.id }}</td>
                  <td>{{ transaction.date }}</td>
                  <td>
                    <span
                      :class="[
                        'px-24 py-4 rounded-pill fw-medium text-sm',
                        transaction.statusClass.bg,
                        transaction.statusClass.text
                      ]"
                    >
                      {{ transaction.status }}
                    </span>
                  </td>
                  <td>{{ transaction.amount }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  
  const transactions = [
    {
      id: '5986124445445',
      date: '27 Mar 2024',
      status: 'Pending',
      statusClass: { bg: 'bg-warning-focus', text: 'text-warning-main' },
      amount: '$20,000.00',
    },
    {
      id: '5986124445445',
      date: '27 Mar 2024',
      status: 'Rejected',
      statusClass: { bg: 'bg-danger-focus', text: 'text-danger-main' },
      amount: '$20,000.00',
    },
    {
      id: '5986124445445',
      date: '27 Mar 2024',
      status: 'Completed',
      statusClass: { bg: 'bg-success-focus', text: 'text-success-main' },
      amount: '$20,000.00',
    },
    {
      id: '5986124445445',
      date: '27 Mar 2024',
      status: 'Completed',
      statusClass: { bg: 'bg-success-focus', text: 'text-success-main' },
      amount: '$20,000.00',
    },
    {
      id: '5986124445445',
      date: '27 Mar 2024',
      status: 'Completed',
      statusClass: { bg: 'bg-success-focus', text: 'text-success-main' },
      amount: '$20,000.00',
    },
  ];
  </script>
  