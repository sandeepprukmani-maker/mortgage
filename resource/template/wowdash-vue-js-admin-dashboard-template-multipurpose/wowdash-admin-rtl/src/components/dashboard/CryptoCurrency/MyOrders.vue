<template>
    <div class="col-xxl-6">
      <div class="card h-100 radius-8 border-0">
        <div class="card-body p-24">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between mb-20">
            <h6 class="mb-2 fw-bold text-lg">My Orders</h6>
            <div class="">
              <select v-model="selectedPeriod" class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8">
                <option>Today</option>
                <option>Monthly</option>
                <option>Weekly</option>
                <option>Today</option>
              </select>
            </div>
          </div>
  
          <div class="table-responsive scroll-sm">
            <table class="table bordered-table mb-0">
              <thead>
                <tr>
                  <th scope="col">Rate</th>
                  <th scope="col">Amount ETH</th>
                  <th scope="col">Price PLN</th>
                  <th scope="col" class="text-center">Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(order, index) in orders" :key="index">
                  <td>
                    <span :class="order.rateClass">{{ order.rate }}</span>
                  </td>
                  <td>{{ order.amountETH }}</td>
                  <td>{{ order.pricePLN }}</td>
                  <td class="text-center line-height-1">
                    <button type="button" class="text-lg text-danger-main remove-btn" @click="removeOrder(index)">
                      <iconify-icon icon="radix-icons:cross-2" class="icon"></iconify-icon>
                    </button>
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
        selectedPeriod: "Today", // The default selected period
        orders: [
          { rate: "0.265415.00", amountETH: 29.4251512, pricePLN: 2.154, rateClass: "text-success-main" },
          { rate: "0.265415.00", amountETH: 29.4251512, pricePLN: 2.154, rateClass: "text-success-main" },
          { rate: "0.265415.00", amountETH: 29.4251512, pricePLN: 2.154, rateClass: "text-danger-main" },
          { rate: "0.265415.00", amountETH: 29.4251512, pricePLN: 2.154, rateClass: "text-success-main" },
          { rate: "0.265415.00", amountETH: 29.4251512, pricePLN: 2.154, rateClass: "text-danger-main" },
          { rate: "0.265415.00", amountETH: 29.4251512, pricePLN: 2.154, rateClass: "text-danger-main" }
        ]
      };
    },
    methods: {
      removeOrder(index) {
        this.orders.splice(index, 1); // Remove the order from the list
      }
    }
  };
  </script>