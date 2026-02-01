<template>
    <div class="col-xxl-8">
      <div class="card h-100">
        <div class="card-header">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
            <h6 class="mb-2 fw-bold text-lg mb-0">Recent Transactions</h6>
            <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
              View All
              <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
            </a>
          </div>
        </div>
        <div class="card-body p-24">
          <div class="table-responsive scroll-sm">
            <table class="table bordered-table mb-0">
              <thead>
                <tr>
                  <th scope="col">SL</th>
                  <th scope="col">Date</th>
                  <th scope="col">Payment Type</th>
                  <th scope="col">Paid Amount</th>
                  <th scope="col">Due Amount</th>
                  <th scope="col">Payable Amount</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(transaction, index) in transactions" :key="index">
                  <td>
                    <span class="text-secondary-light">{{ transaction.sl }}</span>
                  </td>
                  <td>
                    <span class="text-secondary-light">{{ transaction.date }}</span>
                  </td>
                  <td>
                    <span class="text-secondary-light">{{ transaction.paymentType }}</span>
                  </td>
                  <td>
                    <span class="text-secondary-light">{{ transaction.paidAmount }}</span>
                  </td>
                  <td>
                    <span class="text-secondary-light">{{ transaction.dueAmount }}</span>
                  </td>
                  <td>
                    <span class="text-secondary-light">{{ transaction.payableAmount }}</span>
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
          { sl: 1, date: '21 Jun 2024', paymentType: 'Cash', paidAmount: '$0.00', dueAmount: '$150.00', payableAmount: '$150.00' },
          { sl: 2, date: '21 Jun 2024', paymentType: 'Bank', paidAmount: '$570', dueAmount: '$0.00', payableAmount: '$570.00' },
          { sl: 3, date: '21 Jun 2024', paymentType: 'PayPal', paidAmount: '$300.00', dueAmount: '$100.00', payableAmount: '$200.00' },
          { sl: 4, date: '21 Jun 2024', paymentType: 'Cash', paidAmount: '$0.00', dueAmount: '$150.00', payableAmount: '$150.00' },
          { sl: 5, date: '21 Jun 2024', paymentType: 'PayPal', paidAmount: '$300.00', dueAmount: '$100.00', payableAmount: '$200.00' },
        ],
      };
    },
  };
  </script>