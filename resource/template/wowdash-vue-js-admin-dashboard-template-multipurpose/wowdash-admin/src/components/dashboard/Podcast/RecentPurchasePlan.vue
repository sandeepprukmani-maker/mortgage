<template>
    <div class="col-xxl-8">
      <div class="shadow-7 radius-12 bg-base h-100 overflow-hidden">
        <div class="card-header border-bottom bg-base py-16 px-24 d-flex align-items-center justify-content-between">
          <h6 class="text-lg fw-semibold mb-0">Recent Purchase Plan</h6>
          <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
            View All
            <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
          </a>
        </div>
        <div class="card-body p-0">
          <div class="table-responsive scroll-sm">
            <table class="table bordered-table table-py-8 mb-0 rounded-0 border-0">
              <thead>
                <tr>
                  <th class="rounded-0">User</th>
                  <th class="rounded-0">Amount</th>
                  <th class="rounded-0">StartDate</th>
                  <th class="rounded-0">End Date</th>
                  <th class="rounded-0">Duration</th>
                  <th class="rounded-0 text-center">Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(purchase, index) in purchases" :key="index">
                  <td class="text-secondary-light">
                    <div class="d-flex align-items-center gap-12">
                      <span class="w-40-px h-40-px radius-4 overflow-hidden rounded-circle">
                        <img :src="purchase.avatar" alt="Avatar" class="w-100 h-100 object-fit-cover" />
                      </span>
                      <span class="text-secondary-light">{{ purchase.name }}</span>
                    </div>
                  </td>
                  <td class="text-secondary-light">{{ purchase.amount }}</td>
                  <td class="text-secondary-light">{{ purchase.startDate }}</td>
                  <td class="text-secondary-light">{{ purchase.endDate }}</td>
                  <td class="text-secondary-light">{{ purchase.duration }}</td>
                  <td class="text-center">
                    <span :class="purchase.statusClass" class="px-16 py-2 radius-4 fw-medium text-sm">
                      {{ purchase.status }}
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
  import user7 from '@/assets/images/user-grid/user-grid-img7.png'
  import user8 from '@/assets/images/user-grid/user-grid-img8.png'

  export default {
    name: 'RecentPurchasePlan',
    data() {
      return {
        purchases: [
          {
            name: 'Dianne Russell',
            avatar: user5,
            amount: '$29.00',
            startDate: 'Jan 10, 2025',
            endDate: 'Feb 10, 2025',
            duration: '1 Month',
            status: 'Basic',
            statusClass: 'bg-success-focus text-success-main',
          },
          {
            name: 'Cody Fisher',
            avatar: user4,
            amount: '$$99.00',
            startDate: 'Feb 10, 2025',
            endDate: 'April 10, 2025',
            duration: '3 Month',
            status: 'Standard',
            statusClass: 'bg-warning-focus text-warning-main',
          },
          {
            name: 'Ronald Richards',
            avatar: user3,
            amount: '$499.00',
            startDate: 'Jan 10, 2025',
            endDate: 'Jan 10, 2026',
            duration: '1 Year',
            status: 'Premium',
            statusClass: 'bg-info-focus text-info-main',
          },
          {
            name: 'Albert Flores',
            avatar: user2,
            amount: '$29.00',
            startDate: 'Jan 10, 2025',
            endDate: 'Feb 10, 2025',
            duration: '1 Month',
            status: 'Basic',
            statusClass: 'bg-success-focus text-success-main',
          },
          {
            name: 'Cameron Williamson',
            avatar: user1,
            amount: '$99.00',
            startDate: 'Feb 10, 2025',
            endDate: 'April 10, 2025',
            duration: '3 Month',
            status: 'Standard',
            statusClass: 'bg-warning-focus text-warning-main',
          },
          {
            name: 'John Doe',
            avatar: user7,
            amount: '$99.00',
            startDate: 'Feb 10, 2025',
            endDate: 'April 10, 2025',
            duration: '3 Month',
            status: 'Basic',
            statusClass: 'bg-success-focus text-success-main',
          },
          {
            name: 'John Robiul',
            avatar: user8,
            amount: '$99.00',
            startDate: 'Feb 10, 2025',
            endDate: 'April 10, 2025',
            duration: '3 Month',
            status: 'Basic',
            statusClass: 'bg-success-focus text-success-main',
          },
        ],
      };
    },
  };
  </script>
  