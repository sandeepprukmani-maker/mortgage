<template>
    <div class="col-lg-4">
      <div class="shadow-7 radius-12 bg-base h-100 overflow-hidden">
        <div class="card-header border-bottom bg-base py-16 px-24 d-flex align-items-center justify-content-between">
          <h6 class="text-lg fw-semibold mb-0">Top Podcaster</h6>
          <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
            View All
            <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
          </a>
        </div>
        <div class="card-body p-20 d-flex flex-column gap-20">
          <div
            v-for="(podcaster, index) in podcasters"
            :key="index"
            class="d-flex align-items-center justify-content-between gap-3"
          >
            <div class="d-flex align-items-center">
              <img
                :src="podcaster.image"
                alt=""
                class="w-40-px h-40-px rounded-circle flex-shrink-0 me-12 overflow-hidden"
              />
              <div class="flex-grow-1">
                <h6 class="text-md mb-0 fw-medium">{{ podcaster.title }}</h6>
                <span class="text-sm text-secondary-light fw-medium">{{ podcaster.category }}</span>
              </div>
            </div>
            <div class="d-flex align-items-center gap-8">
              <div class="d-flex align-items-center gap-1">
                <span
                  v-for="i in 5"
                  :key="i"
                  class="text-md d-flex line-height-1"
                  :class="i <= podcaster.rating ? 'text-warning-600' : 'text-neutral-300'"
                >
                  <i class="ri-star-fill"></i>
                </span>
              </div>
              <span class="text-primary-light text-sm d-block text-end fw-semibold">
                {{ podcaster.rating.toFixed(2) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import podcaster1 from '@/assets/images/homeThirteen/podcaster-img1.png'
  import podcaster2 from '@/assets/images/homeThirteen/podcaster-img2.png'
  import podcaster3 from '@/assets/images/homeThirteen/podcaster-img3.png'
  import podcaster4 from '@/assets/images/homeThirteen/podcaster-img4.png'
  import podcaster5 from '@/assets/images/homeThirteen/podcaster-img5.png'

  export default {
    name: 'TopPodcaster',
    data() {
      return {
        podcasters: [
          {
            title: 'Digital Assets',
            category: 'UI Design',
            image: podcaster1,
            rating: 5.0
          },
          {
            title: 'Side Project',
            category: 'Business',
            image: podcaster2,
            rating: 3.5
          },
          {
            title: 'Investment',
            category: 'Lifestyle',
            image: podcaster3,
            rating: 2.5
          },
          {
            title: 'Investment',
            category: 'Lifestyle',
            image: podcaster4,
            rating: 4.38
          },
          {
            title: 'Investment',
            category: 'Lifestyle',
            image: podcaster5,
            rating: 1.0
          }
        ]
      }
    }
  }
  </script>
  