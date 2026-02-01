<template>
  <div class="col-xxl-4 col-md-6">
    <div class="card">
      <div class="card-header">
        <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
          <h6 class="mb-2 fw-bold text-lg mb-0">Top Instructors</h6>
          <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
            View All
            <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
          </a>
        </div>
      </div>
      <div class="card-body">
        <div v-for="(instructor, index) in instructors" :key="index" class="d-flex align-items-center justify-content-between gap-3" :class="{'mb-24': index !== instructors.length - 1, 'mb-0': index === instructors.length -1 }">
          <div class="d-flex align-items-center">
            <img :src="instructor.image" alt="" class="w-40-px h-40-px rounded-circle flex-shrink-0 me-12 overflow-hidden">
            <div class="flex-grow-1">
              <h6 class="text-md mb-0 fw-medium">{{ instructor.name }}</h6>
              <span class="text-sm text-secondary-light fw-medium">Agent ID: {{ instructor.agentId }}</span>
            </div>
          </div>
          <div>
            <div class="d-flex align-items-center gap-6 mb-1">
              <span v-for="n in 5" :key="n" class="text-lg text-warning-600 d-flex line-height-1">
                <i class="ri-star-fill"></i>
              </span>
            </div>
            <span class="text-primary-light text-sm d-block text-end">{{ instructor.reviews }} Reviews</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import user1 from "@/assets/images/users/user1.png"
  import user2 from "@/assets/images/users/user2.png"
  import user3 from "@/assets/images/users/user3.png"
  import user4 from "@/assets/images/users/user4.png"
  import user5 from "@/assets/images/users/user5.png"

export default {
  name: 'TopInstructors',
  data() {
    return {
      instructors: [
        {
          name: 'Dianne Russell',
          agentId: '36254',
          image: user1,
          reviews: 25
        },
        {
          name: 'Wade Warren',
          agentId: '36254',
          image: user2,
          reviews: 25
        },
        {
          name: 'Albert Flores',
          agentId: '36254',
          image: user3,
          reviews: 25
        },
        {
          name: 'Bessie Cooper',
          agentId: '36254',
          image: user4,
          reviews: 25
        },
        {
          name: 'Arlene McCoy',
          agentId: '36254',
          image: user5,
          reviews: 25
        },
        {
          name: 'Arlene McCoy',
          agentId: '36254',
          image: user1,
          reviews: 25
        }
      ]
    }
  }
}
</script>