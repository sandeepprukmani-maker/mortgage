<template>
    <div class="col-xxl-8">
      <div class="card h-100">
        <div class="card-header border-bottom bg-base py-16 px-24 d-flex align-items-center justify-content-between">
          <h6 class="text-lg fw-semibold mb-0">Latest Appointments</h6>
          <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
            View All
            <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
          </a>
        </div>
        <div class="card-body p-0">
          <div class="table-responsive scroll-sm">
            <table class="table bordered-table mb-0 rounded-0 border-0">
              <thead>
                <tr>
                  <th scope="col" class="bg-transparent rounded-0">Name</th>
                  <th scope="col" class="bg-transparent rounded-0">ID</th>
                  <th scope="col" class="bg-transparent rounded-0">Date</th>
                  <th scope="col" class="bg-transparent rounded-0">Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(appointment, index) in appointments" :key="index">
                  <td>{{ appointment.name }}</td>
                  <td>{{ appointment.id }}</td>
                  <td>{{ appointment.date }}</td>
                  <td>
                    <span
                      :class="appointment.status === 'Completed'
                        ? 'bg-success-focus text-success-main'
                        : 'bg-danger-focus text-danger-main'"
                      class="px-10 py-4 radius-8 fw-medium text-sm"
                    >
                      {{ appointment.status }}
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
    name: 'LatestAppointments',
    data() {
      return {
        appointments: [
          { name: 'General Checkup', id: '#63254', date: '27 Mar 2024', status: 'Completed' },
          { name: 'Blood test results', id: '3.053 ETH', date: '2h 5m 40s', status: 'Canceled' },
          { name: 'Heart Checkup', id: '3.053 ETH', date: '2h 5m 40s', status: 'Completed' },
          { name: 'Vaccination', id: '3.053 ETH', date: '2h 5m 40s', status: 'Canceled' },
          { name: 'Dental Cleanup', id: '3.053 ETH', date: '2h 5m 40s', status: 'Completed' },
          { name: 'Follow up Appointment', id: '3.053 ETH', date: '2h 5m 40s', status: 'Canceled' }
        ]
      };
    }
  };
  </script>
  