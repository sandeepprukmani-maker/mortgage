<template>
  <div class="col-sm-6">
    <div class="card p-0 overflow-hidden position-relative radius-12">
      <div class="card-header py-16 px-24 bg-base border border-end-0 border-start-0 border-top-0">
        <h6 class="text-lg mb-0">Carousel with progress</h6>
      </div>
      <div class="card-body p-0 position-relative">
        <div class="p-0 progress-carousel dots-style-circle dots-positioned">
          <div class="carousel-container">
            <div class="carousel-track" :style="getSlideStyle()">
              <div v-for="(img, index) in images" :key="index" class="carousel-slide">
                <div class="gradient-overlay bottom-0 start-0 h-100 position-relative">
                  <img :src="img.src" alt="" class="w-100 h-100 object-fit-cover" />
                  <div
                    class="position-absolute start-50 translate-middle-x bottom-0 pb-64 z-1 text-center w-100 max-w-440-px">
                    <h5 class="card-title text-white text-lg mb-6">{{ img.title }}</h5>
                    <p class="card-text text-white mx-auto text-sm">{{ img.description }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="slider-progress">
          <span :style="{ width: progress + '%' }"></span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import img1 from '@/assets/images/carousel/carousel-img4.png';
import img2 from '@/assets/images/carousel/carousel-img2.png';
import img3 from '@/assets/images/carousel/carousel-img3.png';
import img4 from '@/assets/images/carousel/carousel-img1.png';

const images = [
  { src: img1, title: 'Carousel Slide One', description: 'User Interface (UI) and User Experience (UX) Design play key roles in the experience users have when' },
  { src: img2, title: 'Carousel Slide Two', description: 'User Interface (UI) and User Experience (UX) Design play key roles in the experience users have when' },
  { src: img3, title: 'Carousel Slide Three', description: 'User Interface (UI) and User Experience (UX) Design play key roles in the experience users have when' },
  { src: img4, title: 'Carousel Slide Four', description: 'User Interface (UI) and User Experience (UX) Design play key roles in the experience users have when' }
];

const currentSlide = ref(0);
const progress = ref(0);
let interval = null;
let progressInterval = null;

const getSlideStyle = () => {
  return {
    transform: `translateX(-${currentSlide.value * 100}%)`,
    transition: 'transform 0.5s ease-in-out',
    display: 'flex',
  };
};

const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % images.length;
  progress.value = 0;
};

const startAutoplay = () => {
  interval = setInterval(() => {
    nextSlide();
  }, 5000);

  progressInterval = setInterval(() => {
    if (progress.value < 100) {
      progress.value += 2;
    }
  }, 100);
};

onMounted(() => {
  startAutoplay();
});

onBeforeUnmount(() => {
  clearInterval(interval);
  clearInterval(progressInterval);
});
</script>

<style scoped>
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

.slider-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background-color: rgba(255, 255, 255, 0.3);
}

.slider-progress span {
  display: block;
  height: 100%;
  background-color: #487fff;
  transition: width 0.1s linear;
}
</style>
