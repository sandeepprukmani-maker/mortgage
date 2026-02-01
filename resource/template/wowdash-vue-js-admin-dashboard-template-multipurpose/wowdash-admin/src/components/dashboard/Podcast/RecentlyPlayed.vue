<template>
    <div class="col-lg-8">
      <div class="bg-base radius-12 py-20 px-24 shadow-9 h-100 mb-24">
        <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between border-bottom mb-24 pb-16">
          <h6 class="mb-0 fw-bold text-lg">Recently Played</h6>
          <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
            View All
            <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
          </a>
        </div>
        <div class="mt-20">
          <div class="row gy-4">
            <div v-for="(item, index) in podcasts" :key="index" class="col-lg-3 col-sm-6">
              <div>
                <div class="radius-8 overflow-hidden position-relative">
                  <img :src="item.image" alt="Thumb" class="w-100 h-100 object-fit-cover" />
                  <a
                    href="javascript:void(0)"
                    class="w-28-px h-24-px text-white bg-white bg-opacity-50 d-flex justify-content-center align-items-center position-absolute start-0 bottom-0 ms-10 mb-10 radius-6 hover-bg-white hover-text-primary text-sm"
                  >
                    <i class="ri-play-large-fill"></i>
                  </a>
                </div>
                <div class="mt-12">
                  <h6 class="text-md mb-0">{{ item.title }}</h6>
                  <span class="text-sm text-secondary-light">{{ item.author }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import podcast1 from '@/assets/images/home-fourteen/podcast-img1.png'
  import podcast2 from '@/assets/images/home-fourteen/podcast-img2.png'
  import podcast3 from '@/assets/images/home-fourteen/podcast-img3.png'
  import podcast4 from '@/assets/images/home-fourteen/podcast-img4.png'

  export default {
    name: 'RecentlyPlayed',
    data() {
      return {
        podcasts: [
          {
            title: 'Talk show',
            author: 'Esther Howard',
            image: podcast1,
          },
          {
            title: 'Change Life Style',
            author: 'Cameron Williamson',
            image: podcast2,
          },
          {
            title: 'Neon Lights',
            author: 'Leslie Alexander',
            image: podcast3,
          },
          {
            title: 'Product Design',
            author: 'Bessie Cooper',
            image: podcast4,
          },
        ],
      };
    },
  };
  </script>
  