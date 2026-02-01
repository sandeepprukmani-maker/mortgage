<template>
    <div class="col-xxl-6">
      <div class="card h-100">
        <div class="card-body p-24">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between mb-20">
            <h6 class="mb-2 fw-bold text-lg mb-0">Stock Report</h6>
            <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
              View All
              <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
            </a>
          </div>
          <div class="table-responsive scroll-sm">
            <table class="table bordered-table mb-0">
              <thead>
                <tr>
                  <th scope="col">Items</th>
                  <th scope="col">Price</th>
                  <th scope="col">
                    <div class="max-w-112 mx-auto">
                      <span>Stock</span>
                    </div>
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(product, index) in products" :key="index">
                  <td>{{ product.name }}</td>
                  <td>{{ product.price }}</td>
                  <td>
                    <div class="max-w-112 mx-auto">
                      <div class="w-100">
                        <div class="progress progress-sm rounded-pill" role="progressbar" :aria-valuenow="product.stockPercentage" aria-valuemin="0" aria-valuemax="100">
                          <div
                            class="progress-bar rounded-pill"
                            :class="product.stockClass"
                            :style="{ width: product.stockPercentage + '%' }"
                          ></div>
                        </div>
                      </div>
                      <span class="mt-12 text-secondary-light text-sm fw-medium">{{ product.stockLabel }}</span>
                    </div>
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
    name: "StockReport",
    data() {
      return {
        products: [
          {
            name: "Nike Air Shoes",
            price: "$500.00",
            stockPercentage: 0,
            stockClass: "bg-primary-600",
            stockLabel: "Out of Stock",
          },
          {
            name: "Nike Air Shoes",
            price: "$300.00",
            stockPercentage: 40,
            stockClass: "bg-danger-main",
            stockLabel: "18 Low Stock",
          },
          {
            name: "Nike Air Shoes",
            price: "$500.00",
            stockPercentage: 80,
            stockClass: "bg-success-main",
            stockLabel: "80 High Stock",
          },
          {
            name: "Nike Air Shoes",
            price: "$300.00",
            stockPercentage: 50,
            stockClass: "bg-success-main",
            stockLabel: "50 High Stock",
          },
          {
            name: "Nike Air Shoes",
            price: "$150.00",
            stockPercentage: 70,
            stockClass: "bg-success-main",
            stockLabel: "70 High Stock",
          },
        ],
      };
    },
  };
  </script>
  