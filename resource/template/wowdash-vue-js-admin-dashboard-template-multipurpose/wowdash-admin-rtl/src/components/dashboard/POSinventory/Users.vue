<template>
    <div class="col-xxl-4 col-md-6">
      <div class="card">
        <div class="card-header border-bottom">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
            <h6 class="mb-2 fw-bold text-lg mb-0">Users</h6>
            <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
              View All
              <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
            </a>
          </div>
        </div>
        <div class="card-body p-20">
          <div class="d-flex flex-column gap-24">
            <div v-for="(user, index) in users" :key="index" class="d-flex align-items-center justify-content-between gap-3">
              <div class="d-flex align-items-center">
                <img :src="user.image" alt="" class="w-40-px h-40-px rounded-circle flex-shrink-0 me-12 overflow-hidden">
                <div class="flex-grow-1">
                  <h6 class="text-md mb-0">{{ user.name }}</h6>
                  <span class="text-sm text-secondary-light fw-normal">{{ user.role }}</span>
                </div>
              </div>
              <span :class="['fw-medium text-md', user.statusClass]">{{ user.status }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import user1 from '@/assets/images/user-grid/user-grid-img1.png'
  import user2 from '@/assets/images/user-grid/user-grid-img2.png'
  import user3 from '@/assets/images/user-grid/user-grid-img3.png'
  import user4 from '@/assets/images/user-grid/user-grid-img4.png'

  export default {
    name: 'UserCard',
    data() {
      return {
        users: [
          {
            name: 'Psychiatry',
            role: 'Super Admin',
            status: 'Pending',
            statusClass: 'text-warning-main',
            image: user1,
          },
          {
            name: 'Orthopedic',
            role: 'Admin',
            status: 'Active',
            statusClass: 'text-success-main',
            image: user2,
          },
          {
            name: 'Cardiology',
            role: 'Manager',
            status: 'Active',
            statusClass: 'text-success-main',
            image: user3,
          },
          {
            name: 'Pediatrics',
            role: 'Admin',
            status: 'Active',
            statusClass: 'text-success-main',
            image: user4,
          },
          {
            name: 'Neurology',
            role: 'Manager',
            status: 'Active',
            statusClass: 'text-success-main',
            image: user1,
          },
        ],
      };
    },
  };
  </script>
  