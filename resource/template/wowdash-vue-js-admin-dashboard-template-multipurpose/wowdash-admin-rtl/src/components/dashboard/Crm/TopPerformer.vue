<template>
    <div class="col-xxl-4">
      <div class="card">
        <div class="card-body">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
            <h6 class="mb-2 fw-bold text-lg mb-0">Top Performer</h6>
            <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
              View All
              <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
            </a>
          </div>
  
          <div class="mt-32">
            <div
              v-for="(performer, index) in performers"
              :key="index"
              class="d-flex align-items-center justify-content-between gap-3"
              :class="{'mb-32': index !== performers.length - 1, 'mb-0': index === performers.length -1 }"
            >
              <div class="d-flex align-items-center">
                <img
                  :src="performer.image"
                  alt=""
                  class="w-40-px h-40-px rounded-circle flex-shrink-0 me-12 overflow-hidden"
                />
                <div class="flex-grow-1">
                  <h6 class="text-md mb-0">{{ performer.name }}</h6>
                  <span class="text-sm text-secondary-light fw-medium">Agent ID: {{ performer.agentId }}</span>
                </div>
              </div>
              <span class="text-primary-light text-md fw-medium">{{ performer.score }}</span>
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
    name: 'TopPerformerCard',
    data() {
      return {
        performers: [
          {
            name: 'Dianne Russell',
            agentId: '36254',
            score: '60/80',
            image: user1
          },
          {
            name: 'Wade Warren',
            agentId: '36254',
            score: '50/70',
            image: user2
          },
          {
            name: 'Albert Flores',
            agentId: '36254',
            score: '55/75',
            image: user3
          },
          {
            name: 'Bessie Cooper',
            agentId: '36254',
            score: '60/80',
            image: user4
          },
          {
            name: 'Arlene McCoy',
            agentId: '36254',
            score: '55/75',
            image: user5
          },
          {
            name: 'Arlene McCoy',
            agentId: '36254',
            score: '50/70',
            image: user1
          }
        ]
      };
    }
  };
  </script>
  