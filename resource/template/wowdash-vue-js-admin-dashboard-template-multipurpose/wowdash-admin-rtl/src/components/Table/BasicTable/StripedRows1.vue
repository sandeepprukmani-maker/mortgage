<template>
    <div class="col-lg-6">
      <div class="card">
        <div class="card-header">
          <h5 class="card-title mb-0">Striped Rows</h5>
        </div>
        <div class="card-body">
          <div class="table-responsive">
            <table class="table striped-table mb-0">
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
                <tr v-for="(item, index) in tableData" :key="index">
                  <td>
                    <div class="d-flex align-items-center">
                      <img :src="item.image" alt="" class="flex-shrink-0 me-12 radius-8 me-12">
                      <div class="flex-grow-1">
                        <h6 class="text-md mb-0 fw-normal">{{ item.name }}</h6>
                        <span class="text-sm text-secondary-light fw-normal">{{ item.category }}</span>
                      </div>
                    </div>
                  </td>
                  <td>{{ item.price }}</td>
                  <td>{{ item.discount }}</td>
                  <td>{{ item.sold }}</td>
                  <td class="text-center">
                    <span class="bg-success-focus text-success-main px-32 py-4 rounded-pill fw-medium text-sm">70</span>
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
    name: "StripedTable",
    data() {
      return {
        tableData: [
          {
            image: product1,
            name: "Blue t-shirt",
            category: "Fashion",
            price: "$500.00",
            discount: "15%",
            sold: "300"
          },
          {
            image: product2,
            name: "Nike Air Shoe",
            category: "Fashion",
            price: "$150.00",
            discount: "N/A",
            sold: "200"
          },
          {
            image: product3,
            name: "Woman Dresses",
            category: "Fashion",
            price: "$300.00",
            discount: "$50.00",
            sold: "1500"
          },
          {
            image: product4,
            name: "Smart Watch",
            category: "Fashion",
            price: "$400.00",
            discount: "$50.00",
            sold: "700"
          },
          {
            image: product5,
            name: "Hoodie Rose",
            category: "Fashion",
            price: "$300.00",
            discount: "25%",
            sold: "500"
          }
        ]
      };
    }
  };
  </script>
  