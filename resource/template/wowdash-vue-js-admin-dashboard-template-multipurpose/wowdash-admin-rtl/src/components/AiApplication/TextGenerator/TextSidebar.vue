<template>
    <div class="col-xxl-3 col-lg-4">
        <div class="card h-100 p-0">
          <div class="card-body p-0">
            <div class="p-24">
              <router-link to="/text-new-chat"
                class="btn btn-primary text-sm btn-sm px-12 py-12 w-100 radius-8 d-flex align-items-center justify-content-center gap-2">
                <i class="ri-messenger-line"></i>
                New Chat
              </router-link>
            </div>

            <ul class="ai-chat-list scroll-sm pe-24 ps-24 pb-24">
              <li class="mb-16 mt-0"><span class="text-primary-600 text-sm fw-semibold">Today</span></li>
              <li class="mb-16" v-for="(item, index) in todayChats" :key="index">
                <router-link to="/text-generator"
                  class="text-line-1 text-secondary-light text-hover-primary-600">{{ item }}</router-link>
              </li>

              <li class="mb-16 mt-24"><span class="text-primary-600 text-sm fw-semibold">Yesterday</span></li>
              <li class="mb-16" v-for="(item, index) in yesterdayChats" :key="index">
                <router-link to="/text-generator"
                  class="text-line-1 text-secondary-light text-hover-primary-600">{{ item }}</router-link>
              </li>

              <li class="mb-16 mt-24"><span class="text-primary-600 text-sm fw-semibold">17/06/2024</span></li>
              <li class="mb-16" v-for="(item, index) in june17Chats" :key="index">
                <router-link to="/text-generator"
                  class="text-line-1 text-secondary-light text-hover-primary-600">{{ item }}</router-link>
              </li>

              <li class="mb-16 mt-24"><span class="text-primary-600 text-sm fw-semibold">15/06/2024</span></li>
              <li class="mb-0">
                <router-link to="/" class="text-line-1 text-secondary-light text-hover-primary-600">Calorie-dense foods:
                  Needs, healthy</router-link>
              </li>
            </ul>

          </div>
        </div>
      </div>
</template>
<script>
export default {
    data() {
    return {
      todayChats: [
        'UI/UX Design Roadmap write me the roadmap right now',
        'Calorie-dense foods: Needs, healthy',
        'Calorie-dense foods: Needs, healthy',
        'Calorie-dense foods: Needs, healthy',
      ],
      yesterdayChats: [
        'Online School Education Learning',
        'Calorie-dense foods: Needs, healthy',
        'Calorie-dense foods: Needs, healthy',
        'Calorie-dense foods: Needs, healthy',
      ],
      june17Chats: [
        'Online School Education Learning',
        'Calorie-dense foods: Needs, healthy',
        'Calorie-dense foods: Needs, healthy',
        'Calorie-dense foods: Needs, healthy',
      ],
    }
  },
}
</script>