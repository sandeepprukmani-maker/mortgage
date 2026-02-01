<template>
    <div class="card radius-16 mt-24">
      <div class="card-header">
        <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
          <h6 class="mb-2 fw-bold text-lg mb-0">Payment History</h6>
          <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
            View All
            <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
          </a>
        </div>
      </div>
      <div class="card-body">
        <div class="table-responsive scroll-sm">
          <table class="table bordered-table sm-table mb-0">
            <thead>
              <tr>
                <th scope="col">Users</th>
                <th scope="col" class="text-center">Email</th>
                <th scope="col" class="text-center">Transaction ID</th>
                <th scope="col" class="text-center">Amount</th>
                <th scope="col" class="text-center">Payment Method</th>
                <th scope="col" class="text-center">Date</th>
                <th scope="col" class="text-center">Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(payment, index) in payments" :key="index">
                <td>
                  <div class="d-flex align-items-center">
                    <img :src="payment.userImage" alt="" class="w-40-px h-40-px rounded-circle flex-shrink-0 me-12 overflow-hidden" />
                    <div class="flex-grow-1">
                      <h6 class="text-md mb-0 fw-medium">{{ payment.userName }}</h6>
                    </div>
                  </div>
                </td>
                <td class="text-center">{{ payment.email }}</td>
                <td class="text-center">{{ payment.transactionId }}</td>
                <td class="text-center">${{ payment.amount }}</td>
                <td class="text-center">{{ payment.paymentMethod }}</td>
                <td class="text-center">{{ payment.date }}</td>
                <td class="text-center">
                  <span :class="['bg-success-focus text-success-main px-24 py-4 rounded-pill fw-medium text-sm', payment.statusClass]">
                    {{ payment.status }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import user1 from '@/assets/images/users/user1.png'
  import user2 from '@/assets/images/users/user2.png'
  import user3 from '@/assets/images/users/user3.png'
  import user4 from '@/assets/images/users/user4.png'
  import user5 from '@/assets/images/users/user5.png'

  export default {
    data() {
      return {
        payments: [
          {
            userImage: user1,
            userName: 'Dianne Russell',
            email: 'osgoodwy@gmail.com',
            transactionId: '9562415412263',
            amount: '29.00',
            paymentMethod: 'Bank',
            date: '24 Jun 2024',
            status: 'Active',
            statusClass: 'active'
          },
          {
            userImage: user2,
            userName: 'Wade Warren',
            email: 'redaniel@gmail.com',
            transactionId: '9562415412263',
            amount: '29.00',
            paymentMethod: 'Bank',
            date: '24 Jun 2024',
            status: 'Active',
            statusClass: 'active'
          },
          {
            userImage: user3,
            userName: 'Albert Flores',
            email: 'seema@gmail.com',
            transactionId: '9562415412263',
            amount: '29.00',
            paymentMethod: 'Bank',
            date: '24 Jun 2024',
            status: 'Active',
            statusClass: 'active'
          },
          {
            userImage: user4,
            userName: 'Bessie Cooper',
            email: 'hamli@gmail.com',
            transactionId: '9562415412263',
            amount: '29.00',
            paymentMethod: 'Bank',
            date: '24 Jun 2024',
            status: 'Active',
            statusClass: 'active'
          },
          {
            userImage: user5,
            userName: 'Arlene McCoy',
            email: 'zitka@mail.ru',
            transactionId: '9562415412263',
            amount: '29.00',
            paymentMethod: 'Bank',
            date: '24 Jun 2024',
            status: 'Active',
            statusClass: 'active'
          }
        ]
      }
    }
  }
  </script>