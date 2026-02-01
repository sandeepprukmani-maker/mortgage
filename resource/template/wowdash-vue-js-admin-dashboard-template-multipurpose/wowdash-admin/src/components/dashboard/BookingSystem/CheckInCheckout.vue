<template>
    <div class="card radius-12 border-0">
      <div class="card-body py-48 px-16 d-flex align-items-center justify-content-center gap-100-px">
        <div class="text-center" v-for="(item, index) in progressItems" :key="index">
          <div class="position-relative d-inline-block">
            <svg
              class="radial-progress max-w-120-px"
              :data-percentage="item.percentage"
              viewBox="0 0 80 80"
              ref="progressCircles"
            >
              <circle
                class="incomplete stroke-8-px"
                :class="item.strokeClass"
                cx="40"
                cy="40"
                r="35"
                fill="none"
              ></circle>
              <circle
                class="complete stroke-8-px"
                :class="item.strokeClass"
                cx="40"
                cy="40"
                r="35"
                fill="none"
                :style="{
                  strokeDasharray: circumference,
                  strokeDashoffset: circumference,
                }"
              ></circle>
              <text
                class="percentage"
                x="50%"
                y="57%"
                transform="matrix(0, 1, -1, 0, 80, 0)"
              ></text>
            </svg>
            <span
              class="w-56-px h-56-px rounded-circle bg-neutral-200 text-success-600 d-flex justify-content-center align-items-center position-absolute start-50 top-50 translate-middle"
            >
              <i
                :class="item.iconClass"
                class="w-24-px h-24-px text-md text-white d-flex justify-content-center align-items-center rounded-circle"
              ></i>
            </span>
          </div>
          <div class="mt-24">
            <h5 class="mb-1">{{ item.percentage }}%</h5>
            <span class="text-secondary-light">{{ item.label }}</span>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'RadialProgress',
    data() {
      return {
        circumference: 2 * Math.PI * 35,
        progressItems: [
          {
            percentage: 70,
            strokeClass: 'stroke-green',
            iconClass:
              'ri-contract-left-fill bg-success-600',
            label: 'Check In',
          },
          {
            percentage: 30,
            strokeClass: 'stroke-warning',
            iconClass:
              'ri-contract-right-fill bg-warning-600',
            label: 'Check Out',
          },
        ],
      };
    },
    mounted() {
      window.addEventListener('scroll', this.animateRadials);
      this.animateRadials(); // Trigger on mount too
    },
    beforeUnmount() {
      window.removeEventListener('scroll', this.animateRadials);
    },
    methods: {
      animateRadials() {
        const circles = this.$refs.progressCircles;
  
        if (!circles || circles.length === 0) return;
  
        const toArray = Array.isArray(circles) ? circles : [circles];
  
        toArray.forEach((svg) => {
          const rect = svg.getBoundingClientRect();
          const inView =
            rect.top >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight);
  
          if (inView) {
            const percent = parseFloat(svg.dataset.percentage);
            const completeCircle = svg.querySelector('circle.complete');
            const radius = completeCircle.getAttribute('r');
            const circumference = 2 * Math.PI * radius;
            const offset = circumference - (percent / 100) * circumference;
  
            completeCircle.style.transition = 'stroke-dashoffset 1.25s';
            completeCircle.style.strokeDasharray = circumference;
            completeCircle.style.strokeDashoffset = offset;
          }
        });
      },
    },
  };
  </script>
  