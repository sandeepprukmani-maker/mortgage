<template>
    <div class="col-xxl-8">
      <div class="card h-100">
        <div class="card-header border-bottom bg-base py-16 px-24 d-flex align-items-center justify-content-between">
          <h6 class="text-lg fw-semibold mb-0">Recent Activity</h6>
          <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
            View All
            <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
          </a>
        </div>
        <div class="card-body p-0">
          <div class="table-responsive scroll-sm">
            <table class="table bordered-table mb-0 rounded-0 border-0">
              <thead>
                <tr>
                  <th class="bg-transparent rounded-0">Customer</th>
                  <th class="bg-transparent rounded-0">ID</th>
                  <th class="bg-transparent rounded-0">Retained</th>
                  <th class="bg-transparent rounded-0">Amount</th>
                  <th class="bg-transparent rounded-0">Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(customer, index) in customers" :key="index">
                  <td>
                    <div class="d-flex align-items-center">
                      <img :src="customer.image" alt="" class="w-40-px h-40-px rounded-circle flex-shrink-0 me-12 overflow-hidden" />
                      <div class="flex-grow-1">
                        <h6 class="text-md mb-0">{{ customer.name }}</h6>
                        <span class="text-sm text-secondary-light fw-medium">{{ customer.email }}</span>
                      </div>
                    </div>
                  </td>
                  <td>{{ customer.id }}</td>
                  <td>{{ customer.retained }}</td>
                  <td>{{ customer.amount }}</td>
                  <td>
                    <span :class="`${customer.statusBg} ${customer.statusText} px-10 py-4 radius-8 fw-medium text-sm`">
                      {{ customer.status }}
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
  import user1 from '@/assets/images/user-grid/user-grid-img1.png'
  import user2 from '@/assets/images/user-grid/user-grid-img2.png'
  import user3 from '@/assets/images/user-grid/user-grid-img3.png'
  import user4 from '@/assets/images/user-grid/user-grid-img4.png'
  import user5 from '@/assets/images/user-grid/user-grid-img5.png'

  export default {
    name: 'RecentActivity',
    data() {
      return {
        customers: [
          {
            name: 'Kristin Watson',
            email: 'ulfaha@mail.ru',
            id: '#63254',
            retained: '5 min ago',
            amount: '$12,408.12',
            status: 'Member',
            statusBg: 'bg-success-focus',
            statusText: 'text-success-main',
            image: user1,
          },
          {
            name: 'Theresa Webb',
            email: 'joie@gmail.com',
            id: '#63254',
            retained: '12 min ago',
            amount: '$12,408.12',
            status: 'New Customer',
            statusBg: 'bg-lilac-100',
            statusText: 'text-lilac-600',
            image: user2,
          },
          {
            name: 'Brooklyn Simmons',
            email: 'warn@mail.ru',
            id: '#63254',
            retained: '15 min ago',
            amount: '$12,408.12',
            status: 'Signed Up',
            statusBg: 'bg-warning-focus',
            statusText: 'text-warning-main',
            image: user3,
          },
          {
            name: 'Robert Fox',
            email: 'fellora@mail.ru',
            id: '#63254',
            retained: '17 min ago',
            amount: '$12,408.12',
            status: 'Member',
            statusBg: 'bg-success-focus',
            statusText: 'text-success-main',
            image: user4,
          },
          {
            name: 'Jane Cooper',
            email: 'zitka@mail.ru',
            id: '#63254',
            retained: '25 min ago',
            amount: '$12,408.12',
            status: 'Signed Up',
            statusBg: 'bg-warning-focus',
            statusText: 'text-warning-main',
            image: user5,
          },
        ],
      };
    },
  };
  </script>
  