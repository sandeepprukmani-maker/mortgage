<template>
    <div class="col-xxl-4 col-md-6">
      <div class="shadow-7 radius-12 bg-base h-100 overflow-hidden">
        <div class="card-header border-bottom bg-base py-16 px-24 d-flex align-items-center justify-content-between">
          <h6 class="text-lg fw-semibold mb-0">Trending Episodes</h6>
          <select class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8">
            <option>Yearly</option>
            <option>Monthly</option>
            <option>Weekly</option>
            <option>Today</option>
          </select>
        </div>
        <div class="card-body p-20 d-flex flex-column gap-12">
          <div v-for="(episode, index) in episodes" :key="index" class="d-flex align-items-center justify-content-between gap-3">
            <div class="d-flex align-items-center">
              <img :src="episode.image" alt="" class="w-40-px h-40-px rounded-circle flex-shrink-0 me-12 overflow-hidden" />
              <div class="flex-grow-1">
                <h6 class="text-md mb-0 fw-medium">{{ episode.title }}</h6>
                <span class="text-sm text-secondary-light fw-medium">{{ episode.author }}</span>
              </div>
            </div>
            <div class="text-end d-flex gap-1 justify-content-end flex-column">
              <span>Durations: <span class="fw-semibold text-primary-light">{{ episode.duration }}</span></span>
              <span>Views: <span class="fw-semibold text-primary-light">{{ episode.views }}</span></span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import trending1 from '@/assets/images/home-fourteen/trending-img1.png'
  import trending2 from '@/assets/images/home-fourteen/trending-img2.png'
  import trending3 from '@/assets/images/home-fourteen/trending-img3.png'
  import trending4 from '@/assets/images/home-fourteen/trending-img4.png'

  export default {
    name: 'TrendingEpisodes',
    data() {
      return {
        episodes: [
          {
            image: trending1,
            title: 'Product Design',
            author: 'Esther Howand',
            duration: '30:05 mins',
            views: '512k',
          },
          {
            image: trending2,
            title: 'How to Change Your Life',
            author: 'Esther Howand',
            duration: '30:05 mins',
            views: '512k',
          },
          {
            image: trending3,
            title: 'Logo Design',
            author: 'Esther Howand',
            duration: '30:05 mins',
            views: '512k',
          },
          {
            image: trending3,
            title: 'Good Health',
            author: 'Esther Howand',
            duration: '30:05 mins',
            views: '512k',
          },
          {
            image: trending4,
            title: 'Episodes Name',
            author: 'Esther Howand',
            duration: '30:05 mins',
            views: '512k',
          },
        ],
      };
    },
  };
  </script>
  