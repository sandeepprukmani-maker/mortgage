<template>
    <div class="col-xxl-4 col-md-6">
      <div class="shadow-7 p-16 radius-12 bg-base">
        <div class="row g-3">
          <div class="col-sm-6 col-xs-6" v-for="(card, index) in cards" :key="index">
            <div
              class="py-20 px-24 radius-8 position-relative z-1 h-100"
              :class="card.bgClass"
            >
              <img
                :src="card.bigIcon"
                alt="Big Icon"
                class="position-absolute end-0 bottom-0"
                :class="card.bigIconClass"
              />
              <span
                class="w-44-px h-44-px radius-8 bg-white d-flex justify-content-center align-items-center"
              >
                <img :src="card.icon" alt="Icon" />
              </span>
              <span class="d-block mt-12 text-neutral-800">{{ card.label }}</span>
              <h6 class="mt-1 mb-0">{{ card.value }}</h6>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import icon1 from '@/assets/images/home-twelve/icons/booking-card-icon1.png'
  import icon2 from '@/assets/images/home-twelve/icons/booking-card-icon2.png'
  import icon3 from '@/assets/images/home-twelve/icons/booking-card-icon3.png'
  import icon4 from '@/assets/images/home-twelve/icons/booking-card-icon4.png'

  import bigIcon1 from '@/assets/images/home-twelve/icons/booking-card-big-icon1.png'
  import bigIcon2 from '@/assets/images/home-twelve/icons/booking-card-big-icon2.png'
  import bigIcon3 from '@/assets/images/home-twelve/icons/booking-card-big-icon3.png'
  import bigIcon4 from '@/assets/images/home-twelve/icons/booking-card-big-icon4.png'
  export default {
    name: 'BookingCards',
    data() {
      return {
        cards: [
          {
            label: 'New Booking',
            value: 170,
            icon: icon1,
            bigIcon: bigIcon1,
            bgClass: 'bg-blue-light',
            bigIconClass: 'me-8 z-n1',
          },
          {
            label: 'Schedule Room',
            value: 285,
            icon: icon2,
            bigIcon: bigIcon2,
            bgClass: 'bg-green-light',
            bigIconClass: 'me-4 z-n1',
          },
          {
            label: 'Total Customers',
            value: 175,
            icon: icon3,
            bigIcon: bigIcon3,
            bgClass: 'bg-red-light',
            bigIconClass: 'me-8 z-n1',
          },
          {
            label: 'Total Revenue',
            value: '$750.00',
            icon: icon4,
            bigIcon: bigIcon4,
            bgClass: 'bg-warning-light',
            bigIconClass: 'me-8 z-n1',
          },
        ],
      };
    },
  };
  </script>
  