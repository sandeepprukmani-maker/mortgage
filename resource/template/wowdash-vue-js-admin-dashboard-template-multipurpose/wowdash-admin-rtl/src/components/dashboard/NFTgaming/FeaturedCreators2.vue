<template>
    <div class="col-xxl-12 col-md-6">
      <div class="card h-100">
        <div class="card-header border-bottom d-flex align-items-center flex-wrap gap-2 justify-content-between">
          <h6 class="fw-bold text-lg mb-0">Featured Creators</h6>
          <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
            View All
            <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
          </a>
        </div>
        <div class="card-body pt-24">
          <div v-for="(creator, index) in creators" :key="index" class="d-flex align-items-center justify-content-between gap-8 flex-wrap" :class="{'mb-32': index !== creators.length - 1, 'mb-0': index === creators.length -1 }">
            <div class="d-flex align-items-center">
              <img :src="creator.img" alt="" class="flex-shrink-0 me-12 w-40-px h-40-px rounded-circle me-12">
              <div class="flex-grow-1">
                <h6 class="text-md mb-0 fw-semibold">{{ creator.name }}</h6>
                <span class="text-sm text-secondary-light fw-normal">{{ creator.username }}</span>
              </div>
            </div>
            <button
              :class="['btn', followBtnClass(creator.isFollowing), 'px-24', 'rounded-pill', 'follow-btn', 'transition-2']"
              @click="toggleFollow(creator)">
              {{ followBtnText(creator.isFollowing) }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import creator1 from "@/assets/images/nft/creator-img1.png"
  import creator2 from "@/assets/images/nft/creator-img2.png"
  import creator3 from "@/assets/images/nft/creator-img3.png"
  import creator4 from "@/assets/images/nft/creator-img4.png"
  import creator5 from "@/assets/images/nft/creator-img5.png"

  export default {
    data() {
      return {
        creators: [
          { name: "Theresa Webb", username: "@wishon", img: creator1, isFollowing: false },
          { name: "Arlene McCoy", username: "@nemccoy", img: creator2, isFollowing: false },
          { name: "Kathryn Murphy", username: "@kathrynmur", img: creator3, isFollowing: false },
          { name: "Marvin McKinney", username: "@marvinckin", img: creator4, isFollowing: false },
          { name: "Dianne Russell", username: "@dinne_r", img: creator5, isFollowing: false }
        ]
      };
    },
    methods: {
      toggleFollow(creator) {
        creator.isFollowing = !creator.isFollowing;
      },
      followBtnText(isFollowing) {
        return isFollowing ? 'Unfollow' : 'Follow';
      },
      followBtnClass(isFollowing) {
        return isFollowing ? 'bg-neutral-200 border-neutral-200 text-neutral-900' : 'bg-primary-600 border-primary-600 text-white';
      }
    }
  };
  </script>
  
  <style scoped>
  /* You can keep your original CSS or add custom styles here */
  </style>
  