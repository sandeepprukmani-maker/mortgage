<template>
    <div class="col-xxl-4 col-sm-6">
      <div class="card h-100">
        <div class="card-body p-24">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between mb-20">
            <h6 class="mb-2 fw-bold text-lg">My Tasks</h6>
            <div class="">
              <select class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8" v-model="selectedStatus">
                <option>All Tasks</option>
                <option>Pending</option>
                <option>Completed</option>
                <option>In Progress</option>
                <option>Canceled</option>
              </select>
            </div>
          </div>
  
          <div class="table-responsive scroll-sm">
            <table class="table bordered-table mb-0 border-neutral-50">
              <thead>
                <tr>
                  <th scope="col" class="border-neutral-50">Project Name</th>
                  <th scope="col" class="border-neutral-50">Deadline</th>
                  <th scope="col" class="border-neutral-50">Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(task, index) in filteredTasks" :key="index">
                  <td class="border-neutral-50">{{ task.projectName }}</td>
                  <td class="border-neutral-50">{{ task.deadline }}</td>
                  <td class="border-neutral-50 text-center">
                    <span :class="['px-16', 'py-2', 'radius-4', 'fw-medium', 'text-sm', statusClasses(task.status)]">
                      {{ task.status }}
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
    data() {
      return {
        selectedStatus: 'All Tasks',
        tasks: [
          {
            projectName: 'Web Development',
            deadline: '10 Jan 2025',
            status: 'Pending'
          },
          {
            projectName: 'UX/UI Design',
            deadline: '10 Jan 2025',
            status: 'Completed'
          },
          {
            projectName: 'React Development',
            deadline: '10 Jan 2025',
            status: 'InProgress'
          },
          {
            projectName: 'Django Development',
            deadline: '10 Jan 2025',
            status: 'Pending'
          },
          {
            projectName: 'Web Development',
            deadline: '10 Jan 2025',
            status: 'Cancelled'
          },
          {
            projectName: 'Web Design',
            deadline: '10 Jan 2025',
            status: 'InProgress'
          }
        ]
      };
    },
    computed: {
      filteredTasks() {
        if (this.selectedStatus === 'All Tasks') {
          return this.tasks;
        }
        return this.tasks.filter(task => task.status === this.selectedStatus);
      }
    },
    methods: {
      statusClasses(status) {
        switch (status) {
          case 'Pending':
            return 'bg-warning-focus text-warning-main';
          case 'Completed':
            return 'bg-success-focus text-success-main';
          case 'InProgress':
            return 'bg-purple-light text-purple';
          case 'Cancelled':
            return 'bg-danger-focus text-danger-main';
          default:
            return '';
        }
      }
    }
  };
  </script>