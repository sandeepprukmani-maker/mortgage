<template>
    <div class="col-xxl-4">
      <div class="card h-100">
        <div class="card-body p-24">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between mb-20">
            <h6 class="mb-2 fw-bold text-lg">Project Status</h6>
            <div>
              <select class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8">
                <option>Yearly</option>
                <option>Monthly</option>
                <option>Weekly</option>
                <option>Today</option>
              </select>
            </div>
          </div>
  
          <div class="table-responsive scroll-sm">
            <table class="table sm-table bordered-table mb-0">
              <thead>
                <tr>
                  <th scope="col">Name</th>
                  <th scope="col">Duration</th>
                  <th scope="col">
                    <div class="max-w-112 mx-auto">
                      <span>Stock</span>
                    </div>
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in projectStatus" :key="index">
                  <td>{{ item.name }}</td>
                  <td>{{ item.duration }}</td>
                  <td>
                    <div class="max-w-112 mx-auto">
                      <div class="w-100">
                        <div 
                          class="progress progress-sm rounded-pill" 
                          role="progressbar" 
                          aria-label="Success example" 
                          :aria-valuenow="item.progress" 
                          aria-valuemin="0" 
                          aria-valuemax="100"
                        >
                          <div 
                            class="progress-bar rounded-pill" 
                            :class="item.color" 
                            :style="{ width: item.progress + '%' }"
                          ></div>
                        </div>
                      </div>
                      <span class="mt-8 text-secondary-light text-sm fw-medium">{{ item.progress }}%</span>
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
  export default {
    name: 'ProjectStatus',
    data() {
      return {
        projectStatus: [
          { name: 'Gold', duration: '2 Months', progress: 30, color: 'bg-red' },
          { name: 'Dollars', duration: '3 Months', progress: 50, color: 'bg-warning-main' },
          { name: 'Stock Market', duration: '1 Months', progress: 60, color: 'bg-info-main' },
          { name: 'Dimond', duration: '5 Months', progress: 80, color: 'bg-success-main' },
          { name: 'S&P 500', duration: '4 Months', progress: 70, color: 'bg-red' }
        ]
      };
    }
  };
  </script>
  