<template>
    <div class="row gy-4">
      <div class="col-xxl-3 col-sm-6" v-for="(card, index) in cards" :key="index">
        <div :class="`card p-3 shadow-2 radius-8 h-100 ${card.gradient} border border-white`">
          <div class="card-body p-0">
            <div class="d-flex flex-wrap align-items-center justify-content-between gap-1 mb-8">
              <div class="d-flex align-items-center gap-10">
                <span
                  :class="`mb-0 w-48-px h-48-px ${card.bgColor} flex-shrink-0 text-white d-flex justify-content-center align-items-center rounded-circle h6 mb-0`"
                >
                  <img :src="card.icon" alt="" />
                </span>
                <div>
                  <span class="fw-medium text-secondary-light text-md">{{ card.title }}</span>
                  <h6 class="fw-semibold mt-2">{{ card.amount }}</h6>
                </div>
              </div>
            </div>
            <p class="text-sm mb-0 d-flex align-items-center flex-wrap gap-12 mt-12 text-secondary-light">
              <span
                :class="`px-6 py-2 rounded-2 fw-medium text-sm d-flex align-items-center gap-1 ${card.changeBg} ${card.changeText}`"
              >
                <i :class="card.changeIcon"></i> {{ card.changePercent }}
              </span>
              {{ card.subText }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import icon1 from "@/assets/images/home-eleven/icons/home-eleven-icon1.svg"
  import icon2 from "@/assets/images/home-eleven/icons/home-eleven-icon2.svg"
  import icon3 from "@/assets/images/home-eleven/icons/home-eleven-icon3.svg"
  import icon4 from "@/assets/images/home-eleven/icons/home-eleven-icon4.svg"

  export default {
    name: "DashboardCards",
    data() {
      return {
        cards: [
          {
            title: "Total Period Income",
            amount: "$50,000",
            icon: icon1,
            bgColor: "bg-cyan-600",
            gradient: "gradient-deep-two-1",
            changePercent: "95%",
            changeIcon: "ri-arrow-right-up-line",
            changeBg: "bg-success-focus",
            changeText: "text-success-main",
            subText: "Last month $24,000.00",
          },
          {
            title: "Total Period Expenses",
            amount: "$35,000",
            icon: icon2,
            bgColor: "bg-warning-600",
            gradient: "gradient-deep-two-2",
            changePercent: "95%",
            changeIcon: "ri-arrow-right-up-line",
            changeBg: "bg-success-focus",
            changeText: "text-success-main",
            subText: "Last month $1,600.00",
          },
          {
            title: "Net Profit",
            amount: "$50,000",
            icon: icon3,
            bgColor: "bg-lilac-600",
            gradient: "gradient-deep-two-3",
            changePercent: "70%",
            changeIcon: "ri-arrow-right-down-line",
            changeBg: "bg-danger-focus",
            changeText: "text-danger-main",
            subText: "Last month $24,000.00",
          },
          {
            title: "Total Saving",
            amount: "$50,000",
            icon: icon4,
            bgColor: "bg-success-600",
            gradient: "gradient-deep-two-4",
            changePercent: "95%",
            changeIcon: "ri-arrow-right-up-line",
            changeBg: "bg-success-focus",
            changeText: "text-success-main",
            subText: "Last month $2,500.00",
          },
        ],
      };
    },
  };
  </script>
  