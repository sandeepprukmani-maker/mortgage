<template>
    <div class="col-xxl-6">
      <div class="card h-100">
        <div class="card-header border-bottom bg-base ps-0 py-0 pe-24 d-flex align-items-center justify-content-between">
          <ul class="nav bordered-tab nav-pills mb-0" role="tablist">
            <li class="nav-item" role="presentation">
              <button
                class="nav-link"
                :class="{ active: activeTab === 'toDoList' }"
                id="pills-to-do-list-tab"
                type="button"
                role="tab"
                aria-controls="pills-to-do-list"
                aria-selected="true"
                @click="activeTab = 'toDoList'"
              >
                All Item
              </button>
            </li>
            <li class="nav-item" role="presentation">
              <button
                class="nav-link"
                :class="{ active: activeTab === 'recentLeads' }"
                id="pills-recent-leads-tab"
                type="button"
                role="tab"
                aria-controls="pills-recent-leads"
                aria-selected="false"
                tabindex="-1"
                @click="activeTab = 'recentLeads'"
              >
                Best Match
              </button>
            </li>
          </ul>
          <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
            View All
            <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
          </a>
        </div>
  
        <div class="card-body p-24">
          <div class="tab-content">
            <!-- All Item Tab -->
            <div
              class="tab-pane fade"
              :class="{ 'show active': activeTab === 'toDoList' }"
              id="pills-to-do-list"
              role="tabpanel"
              aria-labelledby="pills-to-do-list-tab"
              tabindex="0"
            >
              <div class="table-responsive scroll-sm">
                <table class="table bordered-table mb-0">
                  <thead>
                    <tr>
                      <th scope="col">Task Name</th>
                      <th scope="col">Assigned To</th>
                      <th scope="col">Due Date</th>
                      <th scope="col">Status</th>
                      <th scope="col">Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(item, index) in todoList" :key="index">
                      <td>
                        <div>
                          <span class="text-md d-block line-height-1 fw-medium text-primary-light text-w-200-px">{{ item.task }}</span>
                          <span class="text-sm d-block fw-normal text-secondary-light">{{ item.code }}</span>
                        </div>
                      </td>
                      <td>{{ item.assigned }}</td>
                      <td>{{ item.date }}</td>
                      <td>
                        <span class="bg-success-focus text-success-main px-24 py-4 rounded-pill fw-medium text-sm">Active</span>
                      </td>
                      <td class="text-center text-neutral-700 text-xl">
                        <div class="dropdown">
                          <button type="button" data-bs-toggle="dropdown" aria-expanded="false">
                            <iconify-icon icon="ph:dots-three-outline-vertical-fill" class="icon"></iconify-icon>
                          </button>
                          <ul class="dropdown-menu p-12 border bg-base shadow">
                            <li><a class="dropdown-item px-16 py-8 rounded text-secondary-light bg-hover-neutral-200 text-hover-neutral-900" href="javascript:void(0)">Action</a></li>
                            <li><a class="dropdown-item px-16 py-8 rounded text-secondary-light bg-hover-neutral-200 text-hover-neutral-900" href="javascript:void(0)">Another action</a></li>
                            <li><a class="dropdown-item px-16 py-8 rounded text-secondary-light bg-hover-neutral-200 text-hover-neutral-900" href="javascript:void(0)">Something else here</a></li>
                          </ul>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
  
            <!-- Best Match Tab -->
            <div
              class="tab-pane fade"
              :class="{ 'show active': activeTab === 'recentLeads' }"
              id="pills-recent-leads"
              role="tabpanel"
              aria-labelledby="pills-recent-leads-tab"
              tabindex="0"
            >
              <div class="table-responsive scroll-sm">
                <table class="table bordered-table mb-0">
                  <thead>
                    <tr>
                      <th scope="col">Task Name</th>
                      <th scope="col">Assigned To</th>
                      <th scope="col">Due Date</th>
                      <th scope="col">Status</th>
                      <th scope="col">Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(item, index) in bestMatchList" :key="index">
                      <td>
                        <div>
                          <span class="text-md d-block line-height-1 fw-medium text-primary-light text-w-200-px">{{ item.task }}</span>
                          <span class="text-sm d-block fw-normal text-secondary-light">{{ item.code }}</span>
                        </div>
                      </td>
                      <td>{{ item.assigned }}</td>
                      <td>{{ item.date }}</td>
                      <td>
                        <span class="bg-success-focus text-success-main px-24 py-4 rounded-pill fw-medium text-sm">Active</span>
                      </td>
                      <td class="text-center text-neutral-700 text-xl">
                        <div class="dropdown">
                          <button type="button" data-bs-toggle="dropdown" aria-expanded="false">
                            <iconify-icon icon="ph:dots-three-outline-vertical-fill" class="icon"></iconify-icon>
                          </button>
                          <ul class="dropdown-menu p-12 border bg-base shadow">
                            <li><a class="dropdown-item px-16 py-8 rounded text-secondary-light bg-hover-neutral-200 text-hover-neutral-900" href="javascript:void(0)">Action</a></li>
                            <li><a class="dropdown-item px-16 py-8 rounded text-secondary-light bg-hover-neutral-200 text-hover-neutral-900" href="javascript:void(0)">Another action</a></li>
                            <li><a class="dropdown-item px-16 py-8 rounded text-secondary-light bg-hover-neutral-200 text-hover-neutral-900" href="javascript:void(0)">Something else here</a></li>
                          </ul>
                        </div>
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
  
  <script setup>
  import { ref } from 'vue'
  
  const activeTab = ref('toDoList')
  
  const todoList = [
    { task: 'Hotel Management System', code: '#5632', assigned: 'Kathryn Murphy', date: '27 Mar 2024' },
    { task: 'Hotel Management System', code: '#5632', assigned: 'Darlene Robertson', date: '27 Mar 2024' },
    { task: 'Hotel Management System', code: '#5632', assigned: 'Courtney Henry', date: '27 Mar 2024' },
    { task: 'Hotel Management System', code: '#5632', assigned: 'Jenny Wilson', date: '27 Mar 2024' },
    { task: 'Hotel Management System', code: '#5632', assigned: 'Leslie Alexander', date: '27 Mar 2024' },
  ]
  
  const bestMatchList = [
    { task: 'Hotel Management System', code: '#5632', assigned: 'Kathryn Murphy', date: '27 Mar 2024' },
    { task: 'Hotel Management System', code: '#5632', assigned: 'Darlene Robertson', date: '27 Mar 2024' },
    { task: 'Hotel Management System', code: '#5632', assigned: 'Courtney Henry', date: '27 Mar 2024' },
    { task: 'Hotel Management System', code: '#5632', assigned: 'Jenny Wilson', date: '27 Mar 2024' },
    { task: 'Hotel Management System', code: '#5632', assigned: 'Leslie Alexander', date: '27 Mar 2024' },
  ]
  </script>
  