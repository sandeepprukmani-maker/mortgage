<template>
    <div class="col-xxl-4 col-md-6">
      <div class="card h-100">
        <div class="card-header">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
            <h6 class="mb-2 fw-bold text-lg mb-0">Top Suppliers</h6>
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
                  <th scope="col">Name</th>
                  <th scope="col">Amount</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(supplier, index) in suppliers" :key="index">
                  <td>
                    <span class="text-secondary-light">{{ supplier.sl }}</span>
                  </td>
                  <td>
                    <span class="text-secondary-light">{{ supplier.name }}</span>
                  </td>
                  <td>
                    <span class="text-secondary-light">{{ supplier.amount }}</span>
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
    name: 'TopSuppliersCard',
    data() {
      return {
        suppliers: [
          { sl: 1, name: 'Esther Howard', amount: '$30,00.00' },
          { sl: 2, name: 'Wade Warren', amount: '$40,00.00' },
          { sl: 3, name: 'Jenny Wilson', amount: '$50,00.00' },
          { sl: 4, name: 'Kristin Watson', amount: '$60,00.00' },
          { sl: 5, name: 'Eleanor Pena', amount: '$70,00.00' },
          { sl: 6, name: 'Darlene Robertson', amount: '$80,00.00' },
        ]
      };
    }
  };
  </script>
  