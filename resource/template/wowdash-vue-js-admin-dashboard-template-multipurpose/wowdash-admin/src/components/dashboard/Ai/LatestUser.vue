<template>
    <div class="col-xxl-9 col-xl-12">
      <div class="card h-100">
        <div class="card-body p-24">
          <div class="d-flex flex-wrap align-items-center gap-1 justify-content-between mb-16">
            <ul class="nav border-gradient-tab nav-pills mb-0" id="pills-tab" role="tablist">
              <li class="nav-item" role="presentation">
                <button
                  class="nav-link d-flex align-items-center active"
                  id="pills-to-do-list-tab"
                  data-bs-toggle="pill"
                  data-bs-target="#pills-to-do-list"
                  type="button"
                  role="tab"
                  aria-controls="pills-to-do-list"
                  aria-selected="true"
                >
                  Latest Registered
                  <span
                    class="text-sm fw-semibold py-6 px-12 bg-neutral-500 rounded-pill text-white line-height-1 ms-12 notification-alert"
                  >
                    {{ latestRegisteredCount }}
                  </span>
                </button>
              </li>
              <li class="nav-item" role="presentation">
                <button
                  class="nav-link d-flex align-items-center"
                  id="pills-recent-leads-tab"
                  data-bs-toggle="pill"
                  data-bs-target="#pills-recent-leads"
                  type="button"
                  role="tab"
                  aria-controls="pills-recent-leads"
                  aria-selected="false"
                  tabindex="-1"
                >
                  Latest Subscribe
                  <span
                    class="text-sm fw-semibold py-6 px-12 bg-neutral-500 rounded-pill text-white line-height-1 ms-12 notification-alert"
                  >
                    {{ latestSubscribeCount }}
                  </span>
                </button>
              </li>
            </ul>
            <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
              View All
              <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
            </a>
          </div>
  
          <div class="tab-content" id="pills-tabContent">
            <div
              class="tab-pane fade show active"
              id="pills-to-do-list"
              role="tabpanel"
              aria-labelledby="pills-to-do-list-tab"
              tabindex="0"
            >
              <div class="table-responsive scroll-sm">
                <table class="table bordered-table sm-table mb-0">
                  <thead>
                    <tr>
                      <th scope="col">Users</th>
                      <th scope="col">Registered On</th>
                      <th scope="col">Plan</th>
                      <th scope="col" class="text-center">Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="user in latestRegisteredUsers" :key="user.email">
                      <td>
                        <div class="d-flex align-items-center">
                          <img :src="user.avatar" alt="" class="w-40-px h-40-px rounded-circle flex-shrink-0 me-12 overflow-hidden" />
                          <div class="flex-grow-1">
                            <h6 class="text-md mb-0 fw-medium">{{ user.name }}</h6>
                            <span class="text-sm text-secondary-light fw-medium">{{ user.email }}</span>
                          </div>
                        </div>
                      </td>
                      <td>{{ user.registeredOn }}</td>
                      <td>{{ user.plan }}</td>
                      <td class="text-center">
                        <span class="bg-success-focus text-success-main px-24 py-4 rounded-pill fw-medium text-sm">Active</span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div
              class="tab-pane fade"
              id="pills-recent-leads"
              role="tabpanel"
              aria-labelledby="pills-recent-leads-tab"
              tabindex="0"
            >
              <div class="table-responsive scroll-sm">
                <table class="table bordered-table sm-table mb-0">
                  <thead>
                    <tr>
                      <th scope="col">Users</th>
                      <th scope="col">Registered On</th>
                      <th scope="col">Plan</th>
                      <th scope="col" class="text-center">Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="user in latestSubscribeUsers" :key="user.email">
                      <td>
                        <div class="d-flex align-items-center">
                          <img :src="user.avatar" alt="" class="w-40-px h-40-px rounded-circle flex-shrink-0 me-12 overflow-hidden" />
                          <div class="flex-grow-1">
                            <h6 class="text-md mb-0 fw-medium">{{ user.name }}</h6>
                            <span class="text-sm text-secondary-light fw-medium">{{ user.email }}</span>
                          </div>
                        </div>
                      </td>
                      <td>{{ user.registeredOn }}</td>
                      <td>{{ user.plan }}</td>
                      <td class="text-center">
                        <span class="bg-success-focus text-success-main px-24 py-4 rounded-pill fw-medium text-sm">Active</span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
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
    data() {
      return {
        latestRegisteredCount: 35,
        latestSubscribeCount: 35,
        latestRegisteredUsers: [
          { name: "Dianne Russell", email: "redaniel@gmail.com", registeredOn: "27 Mar 2024", plan: "Free", avatar: user1 },
          { name: "Wade Warren", email: "xterris@gmail.com", registeredOn: "27 Mar 2024", plan: "Basic", avatar: user2 },
          { name: "Albert Flores", email: "seannand@mail.ru", registeredOn: "27 Mar 2024", plan: "Standard", avatar: user3 },
          { name: "Bessie Cooper", email: "igerrin@gmail.com", registeredOn: "27 Mar 2024", plan: "Business", avatar: user4 },
          { name: "Arlene McCoy", email: "fellora@mail.ru", registeredOn: "27 Mar 2024", plan: "Enterprise", avatar: user5 }
        ],
        latestSubscribeUsers: [
          { name: "Dianne Russell", email: "redaniel@gmail.com", registeredOn: "27 Mar 2024", plan: "Free", avatar: user1 },
          { name: "Wade Warren", email: "xterris@gmail.com", registeredOn: "27 Mar 2024", plan: "Basic", avatar: user2 },
          { name: "Albert Flores", email: "seannand@mail.ru", registeredOn: "27 Mar 2024", plan: "Standard", avatar: user3 },
          { name: "Bessie Cooper", email: "igerrin@gmail.com", registeredOn: "27 Mar 2024", plan: "Business", avatar: user4 },
          { name: "Arlene McCoy", email: "fellora@mail.ru", registeredOn: "27 Mar 2024", plan: "Enterprise", avatar: user5 }
        ]
      };
    }
  };
  </script>