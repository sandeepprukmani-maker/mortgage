<template>
    <div
  class="col-xxl-4 col-sm-6 pricing-plan-wrapper"
  :class="{
    'z-2 position-relative': plan.popular,
  }"
>
       <div
    class="pricing-plan position-relative radius-24 overflow-hidden border"
    :class="[plan.bgColor, plan.popular ? 'p-32 scale-up shadow-lg' : 'p-24']"
    :style="plan.popular ? 'transform: translateY(-20px); z-index: 2;' : ''"
  >
        <span
          v-if="plan.popular"
          class="bg-white bg-opacity-25 text-white radius-24 py-8 px-24 text-sm position-absolute end-0 top-0 z-1 rounded-start-top-0 rounded-end-bottom-0"
        >
          Popular
        </span>
  
        <div class="d-flex align-items-center gap-16">
          <span class="w-72-px h-72-px d-flex justify-content-center align-items-center radius-16 bg-base">
            <img :src="plan.icon" :alt="plan.name" />
          </span>
          <div>
            <span class="fw-medium text-md" :class="textClass">{{ plan.audience }}</span>
            <h6 class="mb-0" :class="textClass">{{ plan.name }}</h6>
          </div>
        </div>
  
        <p class="mt-16 mb-0 mb-28" :class="textClass">Lorem ipsum dolor sit amet doloroli sitiol conse ctetur adipiscing elit.</p>
        <h3 class="mb-24" :class="textClass">${{ plan.price }} <span class="fw-medium text-md" :class="textClass">/monthly</span></h3>
        <span class="mb-20 fw-medium">What’s included</span>
  
        <ul>
          <li v-for="(feature, index) in plan.features" :key="index" class="d-flex align-items-center gap-16 mb-16">
            <span class="w-24-px h-24-px d-flex justify-content-center align-items-center rounded-circle"
                  :class="checkBgClass">
              <iconify-icon icon="iconamoon:check-light" class="text-white text-lg"></iconify-icon>
            </span>
            <span :class="textClass + ' text-lg'">{{ feature }}</span>
          </li>
        </ul>
  
        <button
          type="button"
          class="text-center border text-sm btn-sm px-12 py-10 w-100 radius-8 mt-28"
          :class="plan.btnColor"
          data-bs-toggle="modal"
          data-bs-target="#exampleModal"
        >
          Get started
        </button>
      </div>
    </div>
  </template>
  
  <script setup>
  const props = defineProps({
    plan: Object,
  })
  
  const textClass = props.plan.textColor || (props.plan.popular ? 'text-white' : 'text-secondary-light')
  const checkBgClass = props.plan.popular ? 'bg-white text-primary-600' : props.plan.btnColor?.split(' ')[0]
  </script>
  <style scoped>
.scale-up {
  transform: scale(1.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
</style>

  