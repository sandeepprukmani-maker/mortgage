<template>
    <div class="col-lg-6">
      <div class="card">
        <div class="card-header">
          <h5 class="card-title mb-0">Striped Rows</h5>
        </div>
        <div class="card-body">
          <div class="table-responsive">
            <table class="table vertical-striped-table mb-0">
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
                    <h6 class="text-md mb-0 fw-normal">{{ item.name }}</h6>
                    <span class="text-sm text-secondary-light fw-normal">{{ item.category }}</span>
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
  export default {
    name: "VerticalStripedTable",
    data() {
      return {
        tableData: [
          {
            name: "Blue t-shirt",
            category: "Fashion",
            price: "$500.00",
            discount: "15%",
            sold: "300"
          },
          {
            name: "Blue t-shirt",
            category: "Fashion",
            price: "$150.00",
            discount: "N/A",
            sold: "200"
          },
          {
            name: "Blue t-shirt",
            category: "Fashion",
            price: "$300.00",
            discount: "$50.00",
            sold: "1500"
          },
          {
            name: "Blue t-shirt",
            category: "Fashion",
            price: "$400.00",
            discount: "$50.00",
            sold: "700"
          },
          {
            name: "Blue t-shirt",
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
  