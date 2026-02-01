<template>
    <div class="custom-bg">
      <div class="container container--xl">
        <div class="d-flex align-items-center justify-content-between py-24">
          <router-link to="/">
            <img src="@/assets/images/logo.png" alt="" />
          </router-link>
          <router-link to="/" class="btn btn-outline-primary-600 text-sm">Go To Home</router-link>
        </div>
  
        <div class="py-res-120">
          <div class="row align-items-center">
            <div class="col-lg-6">
              <h3 class="mb-32 max-w-1000-px">Our site is creating. Keep persistence, we are not far off</h3>
              <p class="text-neutral-500 max-w-700-px text-lg">
                We have been spending extended periods to send off our new site.
                Join our mailing list or follow us on Facebook for get most recent update.
              </p>
  
              <div class="countdown my-56 d-flex align-items-center flex-wrap gap-md-4 gap-3" id="coming-soon">
                <div class="d-flex flex-column align-items-center">
                  <h4 class="countdown-item mb-0 w-110-px fw-medium h-110-px bg-neutral-900 w-100 h-100 rounded-circle text-white aspect-ratio-1 d-flex justify-content-center align-items-center">
                    {{ time.days }}
                  </h4>
                  <span class="text-neutral-500 text-md text-uppercase fw-medium mt-8">Days</span>
                </div>
                <div class="d-flex flex-column align-items-center">
                  <h4 class="countdown-item mb-0 w-110-px fw-medium h-110-px bg-neutral-900 w-100 h-100 rounded-circle text-white aspect-ratio-1 d-flex justify-content-center align-items-center">
                    {{ padded(time.hours) }}
                  </h4>
                  <span class="text-neutral-500 text-md text-uppercase fw-medium mt-8">Hours</span>
                </div>
                <div class="d-flex flex-column align-items-center">
                  <h4 class="countdown-item mb-0 w-110-px fw-medium h-110-px bg-neutral-900 w-100 h-100 rounded-circle text-white aspect-ratio-1 d-flex justify-content-center align-items-center">
                    {{ padded(time.minutes) }}
                  </h4>
                  <span class="text-neutral-500 text-md text-uppercase fw-medium mt-8">Minutes</span>
                </div>
                <div class="d-flex flex-column align-items-center">
                  <h4 class="countdown-item mb-0 w-110-px fw-medium h-110-px bg-neutral-900 w-100 h-100 rounded-circle text-white aspect-ratio-1 d-flex justify-content-center align-items-center">
                    {{ padded(time.seconds) }}
                  </h4>
                  <span class="text-neutral-500 text-md text-uppercase fw-medium mt-8">Seconds</span>
                </div>
              </div>
  
              <div class="mt-24 max-w-500-px text-start">
                <span class="fw-semibold text-neutral-600 text-lg text-hover-neutral-600">
                  Do you want to get update? Please subscribe now
                </span>
                <form action="#" class="mt-16 d-flex gap-16 flex-sm-row flex-column">
                  <input type="email" class="form-control text-start py-24 flex-grow-1" placeholder="wowdash@gmail.com" required />
                  <button type="submit" class="btn btn-primary-600 px-24 flex-shrink-0 d-flex align-items-center justify-content-center gap-8">
                    <i class="ri-notification-2-line"></i> Knock Us
                  </button>
                </form>
              </div>
            </div>
  
            <div class="col-lg-6 d-lg-block d-none">
              <img src="@/assets/images/coming-soon/coming-soon.png" alt="" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "ComingSoon",
    data() {
      return {
        deadline: new Date(Date.now() + 99 * 24 * 60 * 60 * 1000),
        time: {
          total: 0,
          days: 0,
          hours: 0,
          minutes: 0,
          seconds: 0,
        },
        timerInterval: null,
      };
    },
    mounted() {
      this.updateClock();
      this.timerInterval = setInterval(this.updateClock, 1000);
    },
    beforeUnmount() {
      clearInterval(this.timerInterval);
    },
    methods: {
      getTimeRemaining(endtime) {
        const t = Date.parse(endtime) - Date.now();
        const seconds = Math.floor((t / 1000) % 60);
        const minutes = Math.floor((t / 1000 / 60) % 60);
        const hours = Math.floor((t / (1000 * 60 * 60)) % 24);
        const days = Math.floor(t / (1000 * 60 * 60 * 24));
        return {
          total: t,
          days,
          hours,
          minutes,
          seconds,
        };
      },
      updateClock() {
        const t = this.getTimeRemaining(this.deadline);
        this.time = t;
        if (t.total <= 0) {
          clearInterval(this.timerInterval);
        }
      },
      padded(value) {
        return String(value).padStart(2, "0");
      },
    },
  };
  </script>
  