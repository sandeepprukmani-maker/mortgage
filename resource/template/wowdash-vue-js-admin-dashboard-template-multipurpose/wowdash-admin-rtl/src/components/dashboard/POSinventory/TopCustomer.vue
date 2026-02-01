<template>
    <div class="col-xxl-4 col-md-6">
      <div class="card h-100">
        <div class="card-header">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
            <h6 class="mb-2 fw-bold text-lg mb-0">Top Customer</h6>
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
                <tr v-for="(customer, index) in customers" :key="index">
                  <td>
                    <span class="text-secondary-light">{{ index + 1 }}</span>
                  </td>
                  <td>
                    <span class="text-secondary-light">{{ customer.name }}</span>
                  </td>
                  <td>
                    <span class="text-secondary-light">{{ customer.amount }}</span>
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
        customers: [
          { name: 'Savannah Nguyen', amount: '$30,00.00' },
          { name: 'Annette Black', amount: '$40,00.00' },
          { name: 'Theresa Webb', amount: '$50,00.00' },
          { name: 'Marvin McKinney', amount: '$60,00.00' },
          { name: 'Brooklyn Simmons', amount: '$70,00.00' },
          { name: 'Dianne Russell', amount: '$80,00.00' },
        ],
      };
    },
  };
  </script>