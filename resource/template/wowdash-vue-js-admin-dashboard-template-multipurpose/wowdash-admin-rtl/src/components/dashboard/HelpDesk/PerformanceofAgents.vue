<template>
    <div class="col-lg-8">
      <div class="shadow-7 radius-12 bg-base h-100 overflow-hidden">
        <div class="card-header border-bottom bg-base py-16 px-24 d-flex align-items-center justify-content-between">
          <h6 class="text-lg fw-semibold mb-0">Performance of Agents</h6>
          <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
            View All
            <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
          </a>
        </div>
        <div class="card-body p-0">
          <div class="table-responsive scroll-sm">
            <table class="table bordered-table table-py-8 mb-0 rounded-0 border-0">
              <thead>
                <tr>
                  <th scope="col" class="rounded-0">Agent Name</th>
                  <th scope="col" class="rounded-0">ID Number</th>
                  <th scope="col" class="rounded-0">Total Tickets</th>
                  <th scope="col" class="rounded-0">Open Tickets</th>
                  <th scope="col" class="rounded-0">Resolved Ticket</th>
                  <th scope="col" class="rounded-0">Satisfaction Rate</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(agent, index) in agents" :key="index">
                  <td class="text-secondary-light">
                    <div class="d-flex align-items-center gap-12">
                      <span class="w-40-px h-40-px radius-4 overflow-hidden rounded-circle">
                        <img :src="agent.image" alt="Avatar" class="w-100 h-100 object-fit-cover" />
                      </span>
                      <span class="text-secondary-light">{{ agent.name }}</span>
                    </div>
                  </td>
                  <td class="text-secondary-light">{{ agent.id }}</td>
                  <td class="text-secondary-light">{{ agent.total }}</td>
                  <td class="text-secondary-light">{{ agent.open }}</td>
                  <td class="text-secondary-light">{{ agent.resolved }}</td>
                  <td>
                    <div class="max-w-112 mx-auto">
                      <div class="w-100">
                        <div
                          class="progress progress-sm rounded-pill"
                          role="progressbar"
                          :aria-valuenow="agent.satisfaction"
                          aria-valuemin="0"
                          aria-valuemax="100"
                        >
                          <div
                            class="progress-bar rounded-pill"
                            :class="agent.color"
                            :style="{ width: agent.satisfaction + '%' }"
                          ></div>
                        </div>
                      </div>
                      <span class="mt-8 text-black text-sm fw-medium">{{ agent.satisfaction }}%</span>
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
  import user1 from '@/assets/images/users/user1.png'
  import user2 from '@/assets/images/users/user2.png'
  import user3 from '@/assets/images/users/user3.png'
  import user4 from '@/assets/images/users/user4.png'

  export default {
    name: 'PerformanceOfAgents',
    data() {
      return {
        agents: [
          {
            name: 'Dianne Russell',
            image: user1,
            id: 26531,
            total: 300,
            open: 250,
            resolved: 50,
            satisfaction: 30,
            color: 'bg-red'
          },
          {
            name: 'Wade Warren',
            image: user2,
            id: 26531,
            total: 300,
            open: 250,
            resolved: 50,
            satisfaction: 50,
            color: 'bg-warning'
          },
          {
            name: 'Albert Flores',
            image: user3,
            id: 26531,
            total: 300,
            open: 250,
            resolved: 50,
            satisfaction: 60,
            color: 'bg-info-main'
          },
          {
            name: 'Bessie Cooper',
            image: user4,
            id: 26531,
            total: 300,
            open: 250,
            resolved: 50,
            satisfaction: 80,
            color: 'bg-success-main'
          },
          {
            name: 'Arlene McCoy',
            image: user1,
            id: 26531,
            total: 300,
            open: 250,
            resolved: 50,
            satisfaction: 75,
            color: 'bg-red'
          }
        ]
      };
    }
  };
  </script>
  