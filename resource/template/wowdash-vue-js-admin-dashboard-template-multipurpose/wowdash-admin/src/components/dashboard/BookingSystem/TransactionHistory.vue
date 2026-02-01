<template>
    <div class="card radius-12 h-100">
      <div class="card-header border-bottom bg-base py-16 px-24 d-flex align-items-center justify-content-between">
        <h6 class="text-lg fw-semibold mb-0">Transaction History</h6>
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
                <th scope="col" class="rounded-0">Place</th>
                <th scope="col" class="rounded-0">ID</th>
                <th scope="col" class="rounded-0">Duration</th>
                <th scope="col" class="rounded-0">Amount</th>
                <th scope="col" class="rounded-0">Date</th>
                <th scope="col" class="rounded-0">Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in transactions" :key="index">
                <td class="text-secondary-light">
                  <div class="d-flex align-items-center gap-12">
                    <span class="w-40-px h-40-px radius-4 overflow-hidden">
                      <img :src="item.image" alt="Avatar" class="w-100 h-100 object-fit-cover" />
                    </span>
                    <span class="text-secondary-light">{{ item.place }}</span>
                  </div>
                </td>
                <td class="text-secondary-light">{{ item.id }}</td>
                <td class="text-secondary-light">{{ item.duration }}</td>
                <td class="text-secondary-light">{{ item.amount }}</td>
                <td class="text-secondary-light">{{ item.date }}</td>
                <td>
                  <span
                    :class="[
                      'px-20 py-4 radius-4 fw-medium text-sm',
                      item.status === 'Completed'
                        ? 'bg-success-focus text-success-main'
                        : 'bg-warning-focus text-warning-main'
                    ]"
                  >
                    {{ item.status }}
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
import transaction1 from '@/assets/images/home-twelve/transaction-img1.png';
import transaction2 from '@/assets/images/home-twelve/transaction-img2.png';
import transaction3 from '@/assets/images/home-twelve/transaction-img3.png';
import transaction4 from '@/assets/images/home-twelve/transaction-img4.png';
import transaction5 from '@/assets/images/home-twelve/transaction-img5.png';

export default {
  name: 'TransactionHistory',
  data() {
    return {
      transactions: [
        {
          place: 'Grand Palace',
          id: '#1250',
          duration: '5 Days, 6 Nights',
          amount: '$209.00',
          date: '21/09/2025',
          status: 'Completed',
          image: transaction1
        },
        {
          place: 'Paris France',
          id: '#6523',
          duration: '2 Days, 3 Nights',
          amount: '$$570.00',
          date: '21/09/2025',
          status: 'Pending',
          image: transaction2
        },
        {
          place: 'Khaosan Road',
          id: '#1250',
          duration: '5 Days, 6 Nights',
          amount: '$870.00',
          date: '21/09/2025',
          status: 'Completed',
          image: transaction3
        },
        {
          place: 'Wat Phra Kaew',
          id: '#6523',
          duration: '2 Days, 3 Nights',
          amount: '$450.00',
          date: '21/09/2025',
          status: 'Pending',
          image: transaction4
        },
        {
          place: 'Wat Pho',
          id: '#1250',
          duration: '3 Days, 4 Nights',
          amount: '$120.00',
          date: '21/09/2025',
          status: 'Completed',
          image: transaction5
        }
      ]
    };
  }
};
</script>
