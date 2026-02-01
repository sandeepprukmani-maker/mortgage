<template>
    <div class="col-xxl-8">
      <div class="shadow-7 radius-12 bg-base h-100 overflow-hidden">
        <div class="card-header border-bottom bg-base py-16 px-24 d-flex align-items-center justify-content-between">
          <h6 class="text-lg fw-semibold mb-0">Projects Status</h6>
          <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
            View All
            <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
          </a>
        </div>
        <div class="card-body p-24">
          <div class="table-responsive scroll-sm">
            <table class="table bordered-table mb-0">
              <thead>
                <tr>
                  <th scope="col" class="rounded-0">Project Name</th>
                  <th scope="col" class="rounded-0">Clients</th>
                  <th scope="col" class="rounded-0">Budget</th>
                  <th scope="col" class="rounded-0">Duration</th>
                  <th scope="col" class="rounded-0">Progress</th>
                  <th scope="col" class="rounded-0 text-center">Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(project, index) in projects" :key="index">
                  <td class="text-secondary-light">{{ project.name }}</td>
                  <td class="text-secondary-light">{{ project.client }}</td>
                  <td class="text-secondary-light">{{ project.budget }}</td>
                  <td class="text-secondary-light">{{ project.duration }}</td>
                  <td class="text-secondary-light">
                    <span
                      :class="['px-6 py-2 radius-4 fw-semibold text-sm d-inline-flex align-items-center gap-1', project.progressClass]"
                    >
                      <i :class="project.progressIcon"></i>
                      {{ project.progress }}
                    </span>
                  </td>
                  <td class="text-center">
                    <span
                      :class="['px-16 py-2 radius-4 fw-semibold text-sm', project.statusClass]"
                    >
                      {{ project.status }}
                    </span>
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
  export default {
    name: 'ProjectsStatus',
    data() {
      return {
        projects: [
          {
            name: 'UX/UI Design',
            client: 'Robert Fox',
            budget: '$24,000',
            duration: '24 Days',
            progress: '95%',
            progressIcon: 'ri-arrow-right-up-line',
            progressClass: 'bg-success-focus text-success-main',
            status: 'Pending',
            statusClass: 'bg-warning-focus text-warning-main',
          },
          {
            name: 'HTML Developer',
            client: 'Leslie Alexander',
            budget: '$32,700',
            duration: '16 Days',
            progress: '95%',
            progressIcon: 'ri-arrow-left-down-line',
            progressClass: 'bg-danger-focus text-danger-main',
            status: 'Completed',
            statusClass: 'bg-success-focus text-success-main',
          },
          {
            name: 'React Development',
            client: 'Devon Lane',
            budget: '$7,250',
            duration: '7 Days',
            progress: '95%',
            progressIcon: 'ri-arrow-right-up-line',
            progressClass: 'bg-success-focus text-success-main',
            status: 'InProgress',
            statusClass: 'bg-purple-light text-purple',
          },
          {
            name: 'Python Research',
            client: 'Savannah Nguyen',
            budget: '$24,500',
            duration: '3 Days',
            progress: '95%',
            progressIcon: 'ri-arrow-right-up-line',
            progressClass: 'bg-success-focus text-success-main',
            status: 'Pending',
            statusClass: 'bg-warning-focus text-warning-main',
          },
          {
            name: 'Laravel Project',
            client: 'Esther Howard',
            budget: '$30,000',
            duration: '5 Days',
            progress: '95%',
            progressIcon: 'ri-arrow-right-up-line',
            progressClass: 'bg-success-focus text-success-main',
            status: 'Cancelled',
            statusClass: 'bg-danger-focus text-danger-main',
          },
        ]
      }
    }
  }
  </script>
  