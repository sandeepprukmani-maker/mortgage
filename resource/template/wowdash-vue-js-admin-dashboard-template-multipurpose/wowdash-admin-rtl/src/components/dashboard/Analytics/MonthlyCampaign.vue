<template>
    <div class="col-xxl-4">
      <div class="card h-100">
        <div class="card-body p-24">
          <div class="d-flex align-items-start flex-column gap-2">
            <h6 class="mb-2 fw-bold text-lg">Monthly Campaign State</h6>
            <span class="text-secondary-light">7.2k Social visitors</span>
          </div>
  
          <div class="d-flex flex-column gap-32 mt-32">
            <div
              class="d-flex align-items-center justify-content-between gap-3"
              v-for="(item, index) in campaignStats"
              :key="index"
            >
              <div class="d-flex align-items-center gap-3">
                <div
                  :class="`w-40-px h-40-px rounded-circle d-flex justify-content-center align-items-center ${item.bgClass} flex-shrink-0`"
                >
                  <img :src="item.image" alt="" />
                </div>
                <div class="flex-grow-1">
                  <h6 class="text-md mb-0 fw-semibold">{{ item.title }}</h6>
                </div>
              </div>
              <div class="d-flex align-items-center gap-8">
                <span class="text-secondary-light text-md fw-medium">{{ item.value }}</span>
                <span :class="`${item.percentClass} text-md fw-medium`">{{ item.percent }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import social1 from '@/assets/images/home-nine/socials1.png'
  import social2 from '@/assets/images/home-nine/socials2.png'
  import social3 from '@/assets/images/home-nine/socials3.png'
  import social4 from '@/assets/images/home-nine/socials4.png'
  import social5 from '@/assets/images/home-nine/socials5.png'

  export default {
    name: 'MonthlyCampaignState',
    data() {
      return {
        campaignStats: [
          {
            title: 'Email',
            value: '6,200',
            percent: '0.3%',
            percentClass: 'text-success-600',
            bgClass: 'bg-lilac-100',
            image: social1,
          },
          {
            title: 'Clicked',
            value: 'Clicked',
            percent: '1.3%',
            percentClass: 'text-danger-600',
            bgClass: 'bg-warning-100',
            image: social2,
          },
          {
            title: 'Subscribe',
            value: '5,175',
            percent: '0.3%',
            percentClass: 'text-success-600',
            bgClass: 'bg-info-100',
            image: social3,
          },
          {
            title: 'Complaints',
            value: '3,780',
            percent: '0.3%',
            percentClass: 'text-success-600',
            bgClass: 'bg-success-100',
            image: social4,
          },
          {
            title: 'Unsubscribe',
            value: '4,120',
            percent: '0.3%',
            percentClass: 'text-success-600',
            bgClass: 'bg-danger-100',
            image: social5,
          },
          {
            title: 'Subscribe',
            value: '5,175',
            percent: '0.3%',
            percentClass: 'text-success-600',
            bgClass: 'bg-info-100',
            image: social3,
          },
        ],
      };
    },
  };
  </script>
  