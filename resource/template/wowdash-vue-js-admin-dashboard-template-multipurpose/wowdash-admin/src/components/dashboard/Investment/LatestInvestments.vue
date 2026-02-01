<template>
    <div class="col-xxl-6">
      <div class="card h-100">
        <div class="card-body p-24">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between mb-20">
            <h6 class="mb-2 fw-bold text-lg mb-0">Latest Investments</h6>
            <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
              View All
              <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
            </a>
          </div>
          <div class="table-responsive scroll-sm">
            <table class="table bordered-table sm-table mb-0">
              <thead>
                <tr>
                  <th scope="col">Asset</th>
                  <th scope="col">Quantity</th>
                  <th scope="col">Price</th>
                  <th scope="col">Date</th>
                  <th scope="col" class="text-center">Total Orders</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(investment, index) in investments" :key="index">
                  <td>
                    <div class="d-flex align-items-center">
                      <img :src="investment.image" alt="" class="flex-shrink-0 me-12 w-40-px h-40-px radius-8 me-12">
                      <div class="flex-grow-1">
                        <h6 class="text-md mb-0 fw-normal">{{ investment.asset }}</h6>
                        <span class="text-sm text-secondary-light fw-normal">{{ investment.type }}</span>
                      </div>
                    </div>
                  </td>
                  <td>
                    <h6 class="text-md mb-0 fw-normal">{{ investment.quantity }}</h6>
                    <span class="text-sm text-secondary-light fw-normal">{{ investment.unit }}</span>
                  </td>
                  <td>{{ investment.price }}</td>
                  <td>{{ investment.date }}</td>
                  <td class="text-center">
                    <span :class="investment.statusClass + ' px-16 py-4 radius-8 fw-medium text-sm'">{{ investment.status }}</span>
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
  import img1 from '@/assets/images/asset/asset-img1.png'
  import img2 from '@/assets/images/asset/asset-img2.png'
  import img3 from '@/assets/images/asset/asset-img3.png'
  import img4 from '@/assets/images/asset/asset-img4.png'
  import img5 from '@/assets/images/asset/asset-img5.png'
  export default {
    name: 'LatestInvestments',
    data() {
      return {
        investments: [
          {
            asset: 'Gold',
            type: 'Main Asset',
            image: img1,
            quantity: '7500',
            unit: 'Ounces',
            price: '$7,500.00',
            date: '25 May 2024',
            status: 'Completed',
            statusClass: 'bg-success-focus text-success-main'
          },
          {
            asset: 'Dollars',
            type: 'Currency',
            image: img2,
            quantity: '5,40,000',
            unit: 'Dollars',
            price: '$5,40,000.00',
            date: '25 May 2024',
            status: 'In Progress',
            statusClass: 'bg-warning-focus text-warning-main'
          },
          {
            asset: 'Stock Market',
            type: 'Product',
            image: img3,
            quantity: '1500',
            unit: 'Products',
            price: '$50,000.00',
            date: '25 May 2024',
            status: 'Completed',
            statusClass: 'bg-success-focus text-success-main'
          },
          {
            asset: 'Dimond',
            type: 'Asset',
            image: img4,
            quantity: '350',
            unit: 'Ounces',
            price: '$30,000.00',
            date: '25 May 2024',
            status: 'In Progress',
            statusClass: 'bg-warning-focus text-warning-main'
          },
          {
            asset: 'S&P 500',
            type: 'Index',
            image: img5,
            quantity: '24,000',
            unit: 'Shares',
            price: '$63,000.00',
            date: '25 May 2024',
            status: 'Completed',
            statusClass: 'bg-success-focus text-success-main'
          }
        ]
      };
    }
  };
  </script>
  