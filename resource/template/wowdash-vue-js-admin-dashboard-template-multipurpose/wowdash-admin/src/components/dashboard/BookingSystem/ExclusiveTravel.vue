<template>
  <div>
    <div class="d-flex align-items-center justify-content-between mb-16">
      <h6 class="text-lg mb-0">Exclusive Travel Packages</h6>
      <div class="d-flex align-items-center gap-16">
        <button type="button" ref="prevEl"
          class="custom-swiper-prev d-flex align-items-center rounded-circle border border-neutral-400 text-neutral-600 text-2l bg-hover-primary-600 hover-text-white justify-content-center w-40-px h-40-px">
          <i class="ri-arrow-left-s-line"></i>
        </button>
        <button type="button" ref="nextEl"
          class="custom-swiper-button d-flex align-items-center rounded-circle border border-neutral-400 text-neutral-600 text-2xl bg-hover-primary-600 hover-text-white justify-content-center w-40-px h-40-px">
          <i class="ri-arrow-right-s-line"></i>
        </button>
      </div>
    </div>

    <Swiper
      :modules="[Navigation]"
      :slides-per-view="4"
      :loop="true"
      :space-between="24"
      :navigation="{ prevEl: prevEl, nextEl: nextEl }"
      :speed="700"
      class="travel-slider"
    >
      <SwiperSlide v-for="(item, index) in travelPackages" :key="index">
        <div class="bg-base p-6 radius-12">
          <div class="radius-8 overflow-hidden">
            <img :src="item.image" alt="Image" class="w-100 h-100 object-fit-cover" />
          </div>
          <div class="p-8 pt-16">
            <h6 class="text-md mb-1">{{ item.title }}</h6>
            <span class="text-secondary-light">{{ item.duration }}</span>
            <div class="mt-10 d-flex align-items-center justify-content-between gap-10">
              <span class="fw-semibold text-secondary-light text-sm">{{ item.price }}</span>
              <div class="d-flex align-items-center gap-1">
                <span class="text-primary-600 line-height-1 text-md fw-medium">
                  <i class="ri-user-3-line"></i>
                </span>
                <span class="text-sm fw-medium">({{ item.people }})</span>
              </div>
            </div>
          </div>
        </div>
      </SwiperSlide>
    </Swiper>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { Swiper, SwiperSlide } from 'swiper/vue';
import { Navigation } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/navigation';

import travel1 from '@/assets/images/home-twelve/travel-img1.png';
import travel2 from '@/assets/images/home-twelve/travel-img2.png';
import travel3 from '@/assets/images/home-twelve/travel-img3.png';
import travel4 from '@/assets/images/home-twelve/travel-img4.png';

const prevEl = ref(null);
const nextEl = ref(null);

const travelPackages = ref([
  { image: travel1, title: 'Paris', duration: '5 Days, 6 Nights', price: '$12,000', people: 280 },
  { image: travel2, title: 'İstanbul', duration: '6 Days, 7 Nights', price: '$7,000', people: 280 },
  { image: travel3, title: 'London', duration: '4 Days, 5 Nights', price: '$15,000', people: 280 },
  { image: travel4, title: 'Bangkok', duration: '3 Days, 4 Nights', price: '$5,000', people: 220 },
  { image: travel2, title: 'İstanbul', duration: '6 Days, 7 Nights', price: '$7,000', people: 280 },
]);
</script>