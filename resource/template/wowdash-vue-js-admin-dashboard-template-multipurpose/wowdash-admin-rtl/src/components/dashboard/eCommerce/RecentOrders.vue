<template>
    <div class="col-xxl-9 col-lg-6">
      <div class="card h-100">
        <div class="card-body p-24">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between mb-20">
            <h6 class="mb-2 fw-bold text-lg mb-0">Recent Orders</h6>
            <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
              View All
              <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
            </a>
          </div>
          <div class="table-responsive scroll-sm">
            <table class="table bordered-table mb-0">
              <thead>
                <tr>
                  <th scope="col">Users</th>
                  <th scope="col">Invoice</th>
                  <th scope="col">Items</th>
                  <th scope="col">Qty</th>
                  <th scope="col">Amount</th>
                  <th scope="col" class="text-center">Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(order, index) in orders" :key="index">
                  <td>
                    <div class="d-flex align-items-center">
                      <img :src="order.image" alt="" class="flex-shrink-0 me-12 radius-8">
                      <span class="text-lg text-secondary-light fw-semibold flex-grow-1">{{ order.name }}</span>
                    </div>
                  </td>
                  <td>{{ order.invoice }}</td>
                  <td>{{ order.item }}</td>
                  <td>{{ order.qty }}</td>
                  <td>{{ order.amount }}</td>
                  <td class="text-center">
                    <span :class="order.statusClass">{{ order.status }}</span>
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
  import user1 from "@/assets/images/users/user1.png"
  import user2 from "@/assets/images/users/user2.png"
  import user3 from "@/assets/images/users/user3.png"
  import user4 from "@/assets/images/users/user4.png"
  import user5 from "@/assets/images/users/user5.png"

  export default {
    name: "RecentOrders",
    data() {
      return {
        orders: [
          {
            image: user1,
            name: "Dianne Russell",
            invoice: "#6352148",
            item: "iPhone 14 max",
            qty: 2,
            amount: "$5,000.00",
            status: "Paid",
            statusClass: "bg-success-focus text-success-main px-24 py-4 rounded-pill fw-medium text-sm",
          },
          {
            image: user2,
            name: "Wade Warren",
            invoice: "#6352148",
            item: "Laptop HPH",
            qty: 3,
            amount: "$1,000.00",
            status: "Pending",
            statusClass: "bg-warning-focus text-warning-main px-24 py-4 rounded-pill fw-medium text-sm",
          },
          {
            image: user3,
            name: "Albert Flores",
            invoice: "#6352148",
            item: "Smart Watch",
            qty: 7,
            amount: "$1,000.00",
            status: "Shipped",
            statusClass: "bg-info-focus text-info-main px-24 py-4 rounded-pill fw-medium text-sm",
          },
          {
            image: user4,
            name: "Bessie Cooper",
            invoice: "#6352148",
            item: "Nike Air Shoe",
            qty: 1,
            amount: "$3,000.00",
            status: "Canceled",
            statusClass: "bg-danger-focus text-danger-main px-24 py-4 rounded-pill fw-medium text-sm",
          },
          {
            image: user5,
            name: "Arlene McCoy",
            invoice: "#6352148",
            item: "New Headphone",
            qty: 5,
            amount: "$4,000.00",
            status: "Canceled",
            statusClass: "bg-danger-focus text-danger-main px-24 py-4 rounded-pill fw-medium text-sm",
          },
        ],
      };
    },
  };
  </script>
  