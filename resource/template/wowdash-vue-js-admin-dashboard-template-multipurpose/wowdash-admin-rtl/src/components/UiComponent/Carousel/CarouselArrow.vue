<template>
  <div class="col-sm-6">
    <div class="card p-0 overflow-hidden position-relative radius-12">
      <div class="card-header py-16 px-24 bg-base border border-end-0 border-start-0 border-top-0">
        <h6 class="text-lg mb-0">Carousel With Arrows</h6>
      </div>
      <div class="card-body p-0 arrow-carousel">
        <div class="carousel-container">
          <div class="carousel-track" :style="getSlideStyle()">
            <div v-for="(img, index) in images" :key="index" class="carousel-slide">
              <div class="gradient-overlay bottom-0 start-0 h-100">
                <img :src="img.src" alt="" class="w-100 h-100 object-fit-cover">
                <div
                  class="position-absolute start-50 translate-middle-x bottom-0 pb-24 z-1 text-center w-100 max-w-440-px">
                  <h5 class="card-title text-white text-lg mb-6">{{ img.title }}</h5>
                  <p class="card-text text-white mx-auto text-sm">{{ img.description }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <button @click="prevSlide" class="carousel-arrow left-arrow">
          <span class="arrow-icon">&lt;</span>
        </button>
        <button @click="nextSlide" class="carousel-arrow right-arrow">
          <span class="arrow-icon">&gt;</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

import carousel1 from '@/assets/images/carousel/carousel-img2.png';
import carousel2 from '@/assets/images/carousel/carousel-img4.png';
import carousel3 from '@/assets/images/carousel/carousel-img3.png';

const images = [
  {
    src: carousel1,
    title: 'Carousel Slide One',
    description: 'User Interface (UI) and User Experience (UX) Design play key roles in the experience users have when...',
  },
  {
    src: carousel2,
    title: 'Carousel Slide Two',
    description: 'User Interface (UI) and User Experience (UX) Design play key roles in the experience users have when...',
  },
  {
    src: carousel3,
    title: 'Carousel Slide Three',
    description: 'User Interface (UI) and User Experience (UX) Design play key roles in the experience users have when...',
  },
];

const currentSlide = ref(0);

const getSlideStyle = () => {
  return {
    transform: `translateX(-${currentSlide.value * 100}%)`,
    transition: 'transform 0.5s ease-in-out',
  };
};

const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % images.length;
};

const prevSlide = () => {
  currentSlide.value = (currentSlide.value - 1 + images.length) % images.length;
};
</script>

<style scoped>
.arrow-carousel {
  position: relative;
  width: 100%;
  height: 100%;
}

.carousel-container {
  overflow: hidden;
  width: 100%;
}

.carousel-track {
  display: flex;
  width: 100%;
}

.carousel-slide {
  min-width: 100%;
  position: relative;
}

.carousel-slide img {
  object-fit: cover;
  width: 100%;
  height: 100%;
}

.position-absolute {
  position: absolute;
}

.start-50 {
  left: 50%;
  transform: translateX(-50%);
}

.translate-middle-x {
  transform: translateX(-50%);
}

.z-1 {
  z-index: 1;
}

.max-w-440-px {
  max-width: 440px;
}

.pb-24 {
  padding-bottom: 24px;
}

.card-title {
  font-size: 1.25rem;
}

.card-text {
  font-size: 0.875rem;
}

.card-body .text-center {
  color: white;
}

/* Arrows for navigation */
.carousel-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  color: white;
  border: none;
  padding: 10px;
  cursor: pointer;
  z-index: 10;
}

.left-arrow {
  left: 10px;
}

.right-arrow {
  right: 10px;
}

.arrow-icon {
  font-size: 2rem;
}

/* Optional: For responsiveness */
@media (max-width: 768px) {
  .card-body .max-w-440-px {
    max-width: 100%;
  }
}
</style>
