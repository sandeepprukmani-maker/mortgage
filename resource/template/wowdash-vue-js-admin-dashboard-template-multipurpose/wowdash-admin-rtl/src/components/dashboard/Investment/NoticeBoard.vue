<template>
    <div class="col-xxl-4">
      <div class="card h-100">
        <div class="card-body p-24">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between mb-20">
            <h6 class="mb-2 fw-bold text-lg mb-0">Notice board</h6>
            <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
              View All
              <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
            </a>
          </div>
  
          <div v-for="(notice, index) in notices" :key="index" class="d-flex align-items-start gap-2" :class="{'mb-20': index !== notices.length - 1}">
            <img :src="notice.image" alt="" class="flex-shrink-0 w-40-px h-40-px me-12 radius-8 me-12">
            <div class="flex-grow-1">
              <h6 class="text-md mb-1 fw-semibold">{{ notice.name }}</h6>
              <p class="text-sm text-secondary-light fw-medium mb-1">{{ notice.description }}</p>
              <span class="text-sm text-secondary-light fw-normal">{{ notice.date }}</span>
            </div>
          </div>
  
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import img1 from '@/assets/images/notice/board-img1.png'
  import img2 from '@/assets/images/notice/board-img2.png'
  import img3 from '@/assets/images/notice/board-img3.png'
  export default {
    name: 'NoticeBoard',
    data() {
      return {
        notices: [
          {
            name: 'Admin',
            image: img1,
            description: 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum is simply dummy.',
            date: '25 Jan 2024'
          },
          {
            name: 'Kathryn Murphy',
            image: img2,
            description: 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum is simply dummy text of the printing and typesetting industry.',
            date: '25 Jan 2024'
          },
          {
            name: 'Cameron Williamson',
            image: img3,
            description: 'Lorem Ipsum is simply dummy text of the printing Lorem Ipsum is simply dummy text of the printing and typesetting industry.',
            date: '25 Jan 2024'
          }
        ]
      };
    }
  };
  </script>
  