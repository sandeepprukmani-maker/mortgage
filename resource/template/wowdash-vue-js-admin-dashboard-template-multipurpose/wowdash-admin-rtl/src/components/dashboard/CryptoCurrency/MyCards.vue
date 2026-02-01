<template>
  <div class="col-xxl-12 col-lg-6">
    <div class="card h-100 radius-8 border-0">
      <div class="card-body">
        <!-- Title and Button Section -->
        <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between mb-20">
          <h6 class="mb-2 fw-bold text-lg">My Cards</h6>
          <a href="#" class="btn btn-outline-primary d-inline-flex align-items-center gap-2 text-sm btn-sm px-8 py-6">
            <iconify-icon icon="ph:plus-circle" class="icon text-xl"></iconify-icon>
            Button
          </a>
        </div>

        <!-- Carousel Section -->
        <Carousel ref="carousel" :items-to-show="1" :wrap-around="true" :autoplay="false" :mouse-drag="true"
          :touch-drag="true" :transition="500" :pause-autoplay-on-hover="true" class="card-slider" :show-arrows="false"
          @slideChanged="onSlideChange">

          <Slide v-for="(card, index) in cards" :key="index">
            <!-- Outer Padding with Updated Width -->
            <div class="p-20 h-240-px radius-8 overflow-hidden position-relative z-1" style="width: 500px;">
              <!-- Card with Inner Padding -->
              <img src="@/assets/images/card/card-bg.png" alt="Card Background"
                class="position-absolute start-0 top-0 w-100 h-100 object-fit-cover z-n1" />
              <div class="d-flex flex-column justify-content-between h-100">
                <div class="d-flex align-items-center justify-content-between flex-wrap">
                  <h6 class="text-white mb-0">Master Card</h6>
                  <img src="@/assets/images/card/card-logo.png" alt="Card Logo" />
                </div>
                <div>
                  <span class="text-white text-xs text-opacity-75">Credit Card Number</span>
                  <h6 class="text-white text-xl fw-semibold mt-1 mb-0">{{ card.number }}</h6>
                </div>
                <div class="d-flex align-items-center justify-content-between">
                  <div>
                    <span class="text-white text-xs text-opacity-75">Name</span>
                    <h6 class="text-white text-xl fw-semibold mb-0">{{ card.name }}</h6>
                  </div>
                  <div>
                    <span class="text-white text-xs text-opacity-75">Exp. Date</span>
                    <h6 class="text-white text-xl fw-semibold mb-0">{{ card.exp }}</h6>
                  </div>
                </div>
              </div>
            </div>
          </Slide>
        </Carousel>

        <!-- Updated Carousel Indicator Lines -->
        <div class="d-flex justify-content-center mt-3 gap-2">
          <span v-for="(card, index) in cards" :key="'dot-' + index" :style="{
            width: index === currentSlide ? '18px' : '10px',
            height: '3.9px',
            backgroundColor: index === currentSlide ? '#2f80ed' : '#e4f1ff',
            borderRadius: '2px',
            transition: 'all 0.3s',
          }"></span>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { Carousel, Slide } from 'vue3-carousel';
import 'vue3-carousel/dist/carousel.css';

const carousel = ref(null);
const cards = [
  { number: '2356 9854 3652 5612', name: 'Arlene McCoy', exp: '05/26' },
  { number: '4123 7845 6654 9910', name: 'Devon Lane', exp: '09/25' },
  { number: '6589 1245 9856 3341', name: 'Courtney Henry', exp: '12/27' },
];

const currentSlide = ref(0);
let autoplayTimeout = null;

function getTimeoutForSlide(index) {
  return index === 2 ? 2000 : 2000;
}

function scheduleNextSlide() {
  clearTimeout(autoplayTimeout);

  autoplayTimeout = setTimeout(() => {
    const nextSlide = (currentSlide.value + 1) % cards.length;
    carousel.value.slideTo(nextSlide);
    currentSlide.value = nextSlide;
    scheduleNextSlide(); // Recursive call
  }, getTimeoutForSlide(currentSlide.value));
}

function onSlideChange({ currentSlide: slideIndex }) {
  currentSlide.value = slideIndex % cards.length;
}

onMounted(() => {
  scheduleNextSlide();
});

onBeforeUnmount(() => {
  clearTimeout(autoplayTimeout);
});
</script>



<style scoped>
.card-content {
  height: 240px;
  width: 450px;
  border-radius: 8px;
  position: relative;
  overflow: hidden;
  padding: 20px;
}

@media (max-width: 1200px) {
  .card-content {
    width: 100%;
  }
}

@media (max-width: 992px) {
  .card-content {
    height: 220px;
  }
}

@media (max-width: 768px) {
  .card-content {
    height: 200px;
  }
}

@media (max-width: 576px) {
  .card-content {
    height: 180px;
  }

  .text-xl {
    font-size: 0.875rem;
  }

  .btn-sm {
    font-size: 0.75rem;
    padding: 4px 8px;
  }
}
</style>
