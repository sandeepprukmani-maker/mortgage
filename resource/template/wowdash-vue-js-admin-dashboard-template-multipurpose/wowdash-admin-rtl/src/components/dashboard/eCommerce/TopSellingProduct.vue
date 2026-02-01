<template>
    <div class="col-xxl-6">
      <div class="card h-100">
        <div class="card-body p-24">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between mb-20">
            <h6 class="mb-2 fw-bold text-lg mb-0">Top Selling Product</h6>
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
                  <th scope="col">Discount</th>
                  <th scope="col">Sold</th>
                  <th scope="col" class="text-center">Total Orders</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(product, index) in products" :key="index">
                  <td>
                    <div class="d-flex align-items-center">
                      <img :src="product.image" alt="" class="flex-shrink-0 me-12 radius-8">
                      <div class="flex-grow-1">
                        <h6 class="text-md mb-0 fw-normal">{{ product.name }}</h6>
                        <span class="text-sm text-secondary-light fw-normal">{{ product.category }}</span>
                      </div>
                    </div>
                  </td>
                  <td>{{ product.price }}</td>
                  <td>{{ product.discount }}</td>
                  <td>{{ product.sold }}</td>
                  <td class="text-center">
                    <span class="bg-success-focus text-success-main px-32 py-4 rounded-pill fw-medium text-sm">
                      {{ product.totalOrders }}
                    </span>
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
  import product1 from "@/assets/images/product/product-img1.png"
  import product2 from "@/assets/images/product/product-img2.png"
  import product3 from "@/assets/images/product/product-img3.png"
  import product4 from "@/assets/images/product/product-img4.png"
  import product5 from "@/assets/images/product/product-img5.png"

  export default {
    name: "TopSellingProduct",
    data() {
      return {
        products: [
          {
            image: product1,
            name: "Blue t-shirt",
            category: "Fashion",
            price: "$500.00",
            discount: "15%",
            sold: 300,
            totalOrders: 70,
          },
          {
            image: product2,
            name: "Nike Air Shoe",
            category: "Fashion",
            price: "$150.00",
            discount: "N/A",
            sold: 200,
            totalOrders: 70,
          },
          {
            image: product3,
            name: "Woman Dresses",
            category: "Fashion",
            price: "$300.00",
            discount: "$50.00",
            sold: 1500,
            totalOrders: 70,
          },
          {
            image: product4,
            name: "Smart Watch",
            category: "Fashion",
            price: "$400.00",
            discount: "$50.00",
            sold: 700,
            totalOrders: 70,
          },
          {
            image: product5,
            name: "Hoodie Rose",
            category: "Fashion",
            price: "$300.00",
            discount: "25%",
            sold: 500,
            totalOrders: 70,
          },
        ],
      };
    },
  };
  </script>
  