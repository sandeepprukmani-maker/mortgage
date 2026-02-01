<template>
    <div class="col-lg-12">
      <div class="card">
        <div class="card-header">
          <h5 class="card-title mb-0">Tables Border Colors</h5>
        </div>
        <div class="card-body">
          <div class="table-responsive">
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
                <tr v-for="(row, index) in tableData" :key="index">
                  <td>
                    <div class="d-flex align-items-center">
                      <img :src="row.image" alt="" class="flex-shrink-0 me-12 radius-8">
                      <span class="text-lg text-secondary-light fw-semibold flex-grow-1">{{ row.name }}</span>
                    </div>
                  </td>
                  <td>{{ row.invoice }}</td>
                  <td>{{ row.item }}</td>
                  <td>{{ row.qty }}</td>
                  <td>{{ row.amount }}</td>
                  <td class="text-center">
                    <span :class="row.statusClass">{{ row.status }}</span>
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
    name: 'BorderedTable',
    data() {
      return {
        tableData: [
          {
            name: 'Dianne Russell',
            image: user1,
            invoice: '#6352148',
            item: 'iPhone 14 max',
            qty: 2,
            amount: '$5,000.00',
            status: 'Paid',
            statusClass: 'bg-success-focus text-success-main px-24 py-4 rounded-pill fw-medium text-sm'
          },
          {
            name: 'Wade Warren',
            image: user2,
            invoice: '#6352148',
            item: 'Laptop HPH',
            qty: 3,
            amount: '$1,000.00',
            status: 'Pending',
            statusClass: 'bg-warning-focus text-warning-main px-24 py-4 rounded-pill fw-medium text-sm'
          },
          {
            name: 'Albert Flores',
            image: user3,
            invoice: '#6352148',
            item: 'Smart Watch',
            qty: 7,
            amount: '$1,000.00',
            status: 'Shipped',
            statusClass: 'bg-info-focus text-info-main px-24 py-4 rounded-pill fw-medium text-sm'
          },
          {
            name: 'Bessie Cooper',
            image: user4,
            invoice: '#6352148',
            item: 'Nike Air Shoe',
            qty: 1,
            amount: '$3,000.00',
            status: 'Canceled',
            statusClass: 'bg-danger-focus text-danger-main px-24 py-4 rounded-pill fw-medium text-sm'
          },
          {
            name: 'Arlene McCoy',
            image: user5,
            invoice: '#6352148',
            item: 'New Headphone',
            qty: 5,
            amount: '$4,000.00',
            status: 'Canceled',
            statusClass: 'bg-danger-focus text-danger-main px-24 py-4 rounded-pill fw-medium text-sm'
          }
        ]
      };
    }
  };
  </script>
  