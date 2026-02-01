<template>
    <div class="col-xxl-4 col-lg-6">
      <div class="card h-100">
        <div class="card-body">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between mb-20">
            <h6 class="mb-2 fw-bold text-lg mb-0">Top Customers</h6>
            <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
              View All
              <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
            </a>
          </div>
  
          <div class="mt-32">
            <div v-for="(customer, index) in customers" :key="index" class="d-flex align-items-center justify-content-between gap-3":class="{'mb-32': index !== customers.length - 1, 'mb-0': index === customers.length -1 }">
              <div class="d-flex align-items-center gap-2">
                <img :src="customer.image" alt="" class="w-40-px h-40-px radius-8 flex-shrink-0">
                <div class="flex-grow-1">
                  <h6 class="text-md mb-0 fw-normal">{{ customer.name }}</h6>
                  <span class="text-sm text-secondary-light fw-normal">{{ customer.phone }}</span>
                </div>
              </div>
              <span class="text-primary-light text-md fw-medium">Orders: {{ customer.orders }}</span>
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
  import user6 from "@/assets/images/users/user6.png"

  export default {
    name: "TopCustomers",
    data() {
      return {
        customers: [
          {
            image: user6,
            name: "Dianne Russell",
            phone: "017******58",
            orders: 30,
          },
          {
            image: user1,
            name: "Wade Warren",
            phone: "017******58",
            orders: 30,
          },
          {
            image: user2,
            name: "Albert Flores",
            phone: "017******58",
            orders: 35,
          },
          {
            image: user3,
            name: "Bessie Cooper",
            phone: "017******58",
            orders: 20,
          },
          {
            image: user4,
            name: "Arlene McCoy",
            phone: "017******58",
            orders: 25,
          },
          {
            image: user6,
            name: "John Doe",
            phone: "017******58",
            orders: 32,
          },
        ],
      };
    },
  };
  </script>
  