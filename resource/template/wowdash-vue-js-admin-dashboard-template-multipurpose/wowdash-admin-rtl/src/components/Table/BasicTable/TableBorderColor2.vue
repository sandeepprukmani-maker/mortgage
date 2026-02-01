<template>
    <div class="col-lg-6">
      <div class="card">
        <div class="card-header">
          <h5 class="card-title mb-0">Tables Border Colors</h5>
        </div>
        <div class="card-body">
          <div class="table-responsive">
            <table class="table colored-row-table mb-0">
              <thead>
                <tr>
                  <th scope="col" class="bg-base">Registered On</th>
                  <th scope="col" class="bg-base">Users</th>
                  <th scope="col" class="bg-base">Email</th>
                  <th scope="col" class="bg-base">Plan</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, index) in tableData" :key="index">
                  <td :class="row.bgClass">{{ row.date }}</td>
                  <td :class="row.bgClass">
                    <div class="d-flex align-items-center">
                      <img
                        :src="row.image"
                        alt=""
                        class="w-40-px h-40-px rounded-circle flex-shrink-0 me-12 overflow-hidden"
                      />
                      <h6 class="text-md mb-0 fw-medium flex-grow-1">{{ row.name }}</h6>
                    </div>
                  </td>
                  <td :class="row.bgClass">{{ row.email }}</td>
                  <td :class="row.bgClass">{{ row.plan }}</td>
                </tr>
              </tbody>
            </table>
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
    name: "ColoredRowTable",
    data() {
      return {
        tableData: [
          {
            date: "27 Mar 2024",
            name: "Dianne Russell",
            email: "random@gmail.com",
            plan: "Free",
            image: user1,
            bgClass: "bg-primary-light"
          },
          {
            date: "27 Mar 2024",
            name: "Wade Warren",
            email: "random@gmail.com",
            plan: "Basic",
            image: user2,
            bgClass: "bg-success-focus"
          },
          {
            date: "27 Mar 2024",
            name: "Albert Flores",
            email: "random@gmail.com",
            plan: "Standard",
            image: user3,
            bgClass: "bg-info-focus"
          },
          {
            date: "27 Mar 2024",
            name: "Bessie Cooper",
            email: "random@gmail.com",
            plan: "Business",
            image: user4,
            bgClass: "bg-warning-focus"
          },
          {
            date: "27 Mar 2024",
            name: "Arlene McCoy",
            email: "random@gmail.com",
            plan: "Enterprise",
            image: user5,
            bgClass: "bg-danger-focus"
          }
        ]
      };
    }
  };
  </script>
  