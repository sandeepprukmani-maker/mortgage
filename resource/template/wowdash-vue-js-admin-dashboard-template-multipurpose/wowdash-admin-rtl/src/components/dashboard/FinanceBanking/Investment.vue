<template>
  <div class="card radius-16 mt-24">
    <div class="card-header">
      <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
        <h6 class="mb-2 fw-bold text-lg mb-0">Investment</h6>
        <select
          class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8"
          v-model="selectedPeriod"
        >
          <option>Today</option>
          <option>Weekly</option>
          <option>Monthly</option>
          <option>Yearly</option>
        </select>
      </div>
    </div>
    <div class="card-body py-20">
      <p class="text-center text-secondary-light d-flex align-items-center gap-8 justify-content-center">
        Total Investment:
        <span class="fw-semibold text-primary-light">{{ totalInvestment }}</span>
      </p>

      <div class="mt-40 mb-24 text-center pe-110 position-relative max-w-288-px mx-auto">
        <div
          class="w-170-px h-170-px rounded-circle z-1 position-relative d-inline-flex justify-content-center align-items-center border border-white border-width-2-px"
        >
          <img
            src="@/assets/images/home-eleven/bg/radial-bg1.png"
            alt=""
            class="position-absolute top-0 start-0 z-n1 w-100 h-100 object-fit-cover"
          />
          <h5 class="text-white">60%</h5>
        </div>
        <div
          class="w-144-px h-144-px rounded-circle z-1 position-relative d-inline-flex justify-content-center align-items-center border border-white border-width-3-px position-absolute top-0 end-0 mt--36"
        >
          <img
            src="@/assets/images/home-eleven/bg/radial-bg2.png"
            alt=""
            class="position-absolute top-0 start-0 z-n1 w-100 h-100 object-fit-cover"
          />
          <h5 class="text-white">30%</h5>
        </div>
        <div
          class="w-110-px h-110-px rounded-circle z-1 position-relative d-inline-flex justify-content-center align-items-center border border-white border-width-3-px position-absolute bottom-0 start-50 translate-middle-x ms-48"
        >
          <img
            src="@/assets/images/home-eleven/bg/radial-bg3.png"
            alt=""
            class="position-absolute top-0 start-0 z-n1 w-100 h-100 object-fit-cover"
          />
          <h5 class="text-white">10%</h5>
        </div>
      </div>

      <div class="d-flex align-items-center flex-wrap gap-24 justify-content-between">
        <div class="d-flex flex-column align-items-start">
          <div class="d-flex align-items-center gap-2">
            <span class="w-12-px h-12-px rounded-pill bg-primary-600"></span>
            <span class="text-secondary-light text-sm fw-normal">Net Income</span>
          </div>
          <h6 class="text-primary-light fw-semibold mb-0 mt-4 text-lg">{{ netIncome }}</h6>
        </div>
        <div class="d-flex flex-column align-items-start">
          <div class="d-flex align-items-center gap-2">
            <span class="w-12-px h-12-px rounded-pill bg-purple"></span>
            <span class="text-secondary-light text-sm fw-normal">Real State</span>
          </div>
          <h6 class="text-primary-light fw-semibold mb-0 mt-4 text-lg">{{ realState }}</h6>
        </div>
        <div class="d-flex flex-column align-items-start">
          <div class="d-flex align-items-center gap-2">
            <span class="w-12-px h-12-px rounded-pill bg-success-600"></span>
            <span class="text-secondary-light text-sm fw-normal">Business</span>
          </div>
          <h6 class="text-primary-light fw-semibold mb-0 mt-4 text-lg">{{ business }}</h6>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "InvestmentCard",
  data() {
    return {
      selectedPeriod: "Today",
      totalInvestment: "$500",
      netIncome: "$50,000",
      realState: "$150",
      business: "$100",
    };
  },
};
</script>
