<template>
    <div class="col-xxl-3 col-lg-4">
      <div class="card h-100 p-0">
        <div class="card-body p-0">
          <div class="p-24">
            <router-link to="/code-generator-new"
              class="btn btn-primary text-sm btn-sm px-12 py-12 w-100 radius-8 d-flex align-items-center justify-content-center gap-2"
            >
              <i class="ri-messenger-line"></i>
              New Page
            </router-link>
          </div>
  
          <ul class="ai-chat-list scroll-sm pe-24 ps-24 pb-24">
            <li class="mb-16 mt-0">
              <span class="text-primary-600 text-sm fw-semibold">Today</span>
            </li>
            <li
              v-for="(item, index) in today"
              :key="'today-' + index"
              class="mb-16"
            >
              <router-link to="/code-generator"
                class="text-line-1 text-secondary-light text-hover-primary-600"
              >
                {{ item.text }}
              </router-link>
            </li>
  
            <li class="mb-16 mt-24">
              <span class="text-primary-600 text-sm fw-semibold">Yesterday</span>
            </li>
            <li
              v-for="(item, index) in yesterday"
              :key="'yesterday-' + index"
              class="mb-16"
            >
              <router-link to="/code-generator"
                class="text-line-1 text-secondary-light text-hover-primary-600"
              >
                {{ item.text }}
              </router-link>
            </li>
  
            <li class="mb-16 mt-24">
              <span class="text-primary-600 text-sm fw-semibold">17/06/2024</span>
            </li>
            <li
              v-for="(item, index) in june17"
              :key="'june17-' + index"
              class="mb-16"
            >
              <router-link to="/code-generator"
                class="text-line-1 text-secondary-light text-hover-primary-600"
              >
                {{ item.text }}
              </router-link>
            </li>
  
            <li class="mb-16 mt-24">
              <span class="text-primary-600 text-sm fw-semibold">15/06/2024</span>
            </li>
            <li class="mb-0">
              <router-link to="/code-generator"
                class="text-line-1 text-secondary-light text-hover-primary-600"
              >
                Calorie-dense foods: Needs, healthy
              </router-link>
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
        today: [
          { text: "Please create a 5 Column table with HTML Css and js" },
          { text: "Calorie-dense foods: Needs, healthy" },
          { text: "Calorie-dense foods: Needs, healthy" },
          { text: "Calorie-dense foods: Needs, healthy" },
        ],
        yesterday: [
          { text: "Online School Education Learning" },
          { text: "Calorie-dense foods: Needs, healthy" },
          { text: "Calorie-dense foods: Needs, healthy" },
          { text: "Calorie-dense foods: Needs, healthy" },
        ],
        june17: [
          { text: "Online School Education Learning" },
          { text: "Calorie-dense foods: Needs, healthy" },
          { text: "Calorie-dense foods: Needs, healthy" },
          { text: "Calorie-dense foods: Needs, healthy" },
        ],
      };
    },
  };
  </script>
  