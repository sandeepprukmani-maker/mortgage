<template>
  <div class="col-xxl-4 col-sm-6">
    <div class="card h-100">
      <div class="card-body p-24">
        <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between mb-20">
          <h6 class="mb-2 fw-bold text-lg">Team Members</h6>
          <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
            View All
            <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
          </a>
        </div>

        <div class="table-responsive scroll-sm">
          <table class="table bordered-table mb-0 border-neutral-100">
            <thead>
              <tr>
                <th scope="col" class="border-neutral-100">Customer</th>
                <th scope="col" class="border-neutral-100">Task</th>
                <th scope="col" class="border-neutral-100">Progress</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(member, index) in teamMembers" :key="index">
                <td class="border-neutral-100">
                  <div class="d-flex align-items-center gap-12">
                    <img :src="member.image" :alt="member.name" class="object-fit-cover rounded-circle w-40-px h-40-px radius-8 flex-shrink-0 overflow-hidden">
                    <div class="flex-grow-1">
                      <h6 class="text-md mb-0 fw-medium">{{ member.name }}</h6>
                      <span class="text-sm text-secondary-light fw-medium">{{ member.email }}</span>
                    </div>
                  </div>
                </td>
                <td class="border-neutral-100">{{ member.task }}</td>
                <td class="border-neutral-100">
                  <div class="max-w-112 mx-auto">
                    <div class="w-100">
                      <div class="progress progress-sm rounded-pill" role="progressbar"
                           aria-label="Success example"
                           :aria-valuenow="member.progress"
                           aria-valuemin="0"
                           aria-valuemax="100">
                        <div class="progress-bar rounded-start-pill"
                             :class="member.color"
                             :style="{ width: member.progress + '%' }">
                        </div>
                      </div>
                    </div>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import user5 from '@/assets/images/user-grid/user-grid-img5.png' 
import user4 from '@/assets/images/user-grid/user-grid-img4.png' 
import user3 from '@/assets/images/user-grid/user-grid-img3.png' 
import user2 from '@/assets/images/user-grid/user-grid-img2.png' 
import user1 from '@/assets/images/user-grid/user-grid-img1.png' 

export default {
  name: 'TeamMembers',
  data() {
    return {
      teamMembers: [
        {
          name: 'Kristin Watson',
          email: 'ulfaha@mail.ru',
          task: 15,
          progress: 80,
          color: 'bg-purple',
          image: user5,
        },
        {
          name: 'Theresa Webb',
          email: 'joie@gmail.com',
          task: 20,
          progress: 50,
          color: 'bg-warning-main',
          image: user4,
        },
        {
          name: 'Brooklyn Simmons',
          email: 'warn@mail.ru',
          task: 24,
          progress: 60,
          color: 'bg-info-main',
          image: user3,
        },
        {
          name: 'Robert Fox',
          email: 'fellora@mail.ru',
          task: 26,
          progress: 92,
          color: 'bg-success-main',
          image: user2,
        },
        {
          name: 'Jane Cooper',
          email: 'zitka@mail.ru',
          task: 25,
          progress: 25,
          color: 'bg-red',
          image: user1,
        },
      ]
    }
  }
}
</script>