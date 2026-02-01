<template>
    <div class="card radius-12 border-0">
      <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between py-12 px-20 border-bottom border-neutral-200">
        <h6 class="mb-2 fw-bold text-lg">Spend Overview</h6>
        <div>
          <select class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8">
            <option>Yearly</option>
            <option>Monthly</option>
            <option>Weekly</option>
            <option>Today</option>
          </select>
        </div>
      </div>
      <div class="card-body">
        <div class="d-flex flex-column gap-20">
          <div
            v-for="(item, index) in spendItems"
            :key="index"
            class="d-flex align-items-center justify-content-between gap-10"
          >
            <div class="d-flex align-items-center gap-12">
              <span :class="item.bgClass + ' w-40-px h-40-px rounded-circle d-flex justify-content-center align-items-center'">
                <img :src="item.icon" alt="Icon" />
              </span>
              <div>
                <h6 class="text-sm mb-2">{{ item.label }}</h6>
                <span class="text-xs text-secondary-light">{{ item.amount }}</span>
              </div>
            </div>
            <div>
              <span class="text-primary-light text-sm d-block text-end">
                <svg
                  class="radial-progress"
                  :data-percentage="item.percentage"
                  viewBox="0 0 80 80"
                  ref="progressCircles"
                >
                  <circle class="incomplete stroke-8-px" :class="item.strokeClass" cx="40" cy="40" r="35"></circle>
                  <circle
                    class="complete stroke-8-px"
                    :class="item.strokeClass"
                    cx="40"
                    cy="40"
                    r="35"
                    :style="{
                      strokeDasharray: circumference,
                      strokeDashoffset: circumference,
                    }"
                  ></circle>
                  <text class="percentage" x="50%" y="57%" transform="matrix(0, 1, -1, 0, 80, 0)">
                    {{ item.percentage }}
                  </text>
                </svg>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import icon1 from '@/assets/images/home-twelve/icons/spen-icon1.png'
  import icon2 from '@/assets/images/home-twelve/icons/spen-icon2.png'
  import icon4 from '@/assets/images/home-twelve/icons/spen-icon4.png'
  export default {
    name: 'SpendOverview',
    data() {
      return {
        circumference: 2 * Math.PI * 35,
        spendItems: [
          {
            label: 'Flights',
            amount: '$70,570',
            icon: icon1,
            bgClass: 'bg-blue-light-two',
            strokeClass: 'stroke-blue',
            percentage: 20,
          },
          {
            label: 'Hotels',
            amount: '$85,570',
            icon: icon2,
            bgClass: 'bg-red-light-two',
            strokeClass: 'stroke-red',
            percentage: 35,
          },
          {
            label: 'Trains',
            amount: '$15,000',
            icon: icon2,
            bgClass: 'bg-red-light-two',
            strokeClass: 'stroke-warning',
            percentage: 45,
          },
          {
            label: 'Cars',
            amount: '$90,000',
            icon: icon4,
            bgClass: 'bg-green-light-two',
            strokeClass: 'stroke-green',
            percentage: 65,
          },
        ],
      };
    },
    mounted() {
      this.resetAllProgress();
      this.animateRadials();
    },
    methods: {
      resetAllProgress() {
        const circles = this.$refs.progressCircles;
        const all = Array.isArray(circles) ? circles : [circles];
        all.forEach((svg) => {
          const complete = svg.querySelector('circle.complete');
          if (complete) complete.removeAttribute('style');
        });
      },
      animateRadials() {
        this.$nextTick(() => {
          const circles = this.$refs.progressCircles;
          const all = Array.isArray(circles) ? circles : [circles];
  
          all.forEach((svg) => {
            const percent = parseFloat(svg.dataset.percentage);
            const complete = svg.querySelector('circle.complete');
            const radius = complete.getAttribute('r');
            const circumference = 2 * Math.PI * radius;
            const offset = circumference - (percent / 100) * circumference;
  
            complete.style.transition = 'stroke-dashoffset 1.65s';
            complete.style.strokeDasharray = circumference;
            complete.style.strokeDashoffset = offset;
          });
        });
      },
    },
  };
  </script>
  