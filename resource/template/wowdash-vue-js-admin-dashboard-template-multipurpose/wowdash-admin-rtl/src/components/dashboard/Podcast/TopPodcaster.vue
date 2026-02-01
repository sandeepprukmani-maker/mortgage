<template>
    <div class="col-xxl-4 col-md-6">
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
            class="d-flex align-items-center justify-content-between gap-3"
            v-for="(podcaster, index) in podcasters"
            :key="index"
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
            <button
              type="button"
              class="follow-btn rounded px-16 py-6"
              :class="podcaster.following ? 'bg-success-600 text-white' : 'bg-success-100 text-success-600'"
              @click="toggleFollow(index)"
            >
              {{ podcaster.following ? 'Following' : 'Follow' }}
            </button>
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
            following: false,
          },
          {
            title: 'Side Project',
            category: 'Business',
            image: podcaster2,
            following: false,
          },
          {
            title: 'Investment',
            category: 'Lifestyle',
            image: podcaster3,
            following: false,
          },
          {
            title: 'Investment',
            category: 'Lifestyle',
            image: podcaster4,
            following: false,
          },
          {
            title: 'Investment',
            category: 'Lifestyle',
            image: podcaster5,
            following: false,
          },
        ],
      };
    },
    methods: {
      toggleFollow(index) {
        this.podcasters[index].following = !this.podcasters[index].following;
      },
    },
  };
  </script>
  