<template>
    <div class="col-sm-12">
        <div class="card p-0 overflow-hidden position-relative radius-12">
            <div class="card-header py-16 px-24 bg-base border border-end-0 border-start-0 border-top-0">
                <h6 class="text-lg mb-0">Multiple slides</h6>
            </div>
            <div class="card-body py-24 px-16">
                <div class="carousel-container">
                    <div class="carousel-track"
                        :style="{ transform: `translateX(-${currentSlide * (100 / slidesPerView)}%)` }">
                        <div class="carousel-slide" v-for="(img, i) in images" :key="i"
                            :style="{ flex: `0 0 ${100 / slidesPerView}%` }">
                            <img :src="img" class="w-100 h-100 object-fit-cover" alt="" />
                        </div>
                    </div>
                </div>
            </div>
            <div class="custom-pagination mt-6 mb-12 text-center">
                <span v-for="i in 5" :key="i" :class="['dot', currentDot === i - 1 ? 'active' : '']" />
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref, computed } from 'vue';

import multipleCarousel1 from '@/assets/images/carousel/mutiple-carousel-img1.png';
import multipleCarousel2 from '@/assets/images/carousel/mutiple-carousel-img2.png';
import multipleCarousel3 from '@/assets/images/carousel/mutiple-carousel-img3.png';
import multipleCarousel4 from '@/assets/images/carousel/mutiple-carousel-img4.png';

const images = [
    multipleCarousel1,
    multipleCarousel2,
    multipleCarousel3,
    multipleCarousel4,
    multipleCarousel1,
    multipleCarousel2,
    multipleCarousel4,
    multipleCarousel3,
];

const currentSlide = ref(0);
const currentDot = ref(0);
const slidesPerView = ref(4);
let interval = null;

const totalDots = computed(() => 5);

const updateSlidesPerView = () => {
    if (window.innerWidth <= 768) {
        slidesPerView.value = 1;
    } else {
        slidesPerView.value = 4;
    }
};

onMounted(() => {
    updateSlidesPerView();
    window.addEventListener('resize', updateSlidesPerView);
    startAutoplay();
});

onBeforeUnmount(() => {
    window.removeEventListener('resize', updateSlidesPerView);
    clearInterval(interval);
});

function startAutoplay() {
    interval = setInterval(() => {
        currentSlide.value = (currentSlide.value + 1) % (images.length - slidesPerView.value + 1);
        currentDot.value = (currentDot.value + 1) % totalDots.value;
    }, 3000);
}

function goToSlide(index) {
    currentSlide.value = index * slidesPerView.value;
    currentDot.value = index;
}
</script>

<style scoped>
.carousel-container {
    overflow: hidden;
    width: 100%;
}

.carousel-track {
    display: flex;
    transition: transform 0.5s ease-in-out;
    width: 100%;
}

.carousel-slide {
    padding: 0 10px;
    box-sizing: border-box;
}

.carousel-slide img {
    width: 100%;
    height: auto;
    border-radius: 8px;
}

.custom-pagination {
    display: flex;
    justify-content: center;
    gap: 5px;
    padding-bottom: 17px;
}

.dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: #5a75ae;
    transition: background-color 0.3s ease;
}

.dot.active {
    width: 11px;
    height: 11px;
    background-color: #487fff;
}

@media (max-width: 768px) {
    .carousel-slide {
        flex: 0 0 100%;
    }
}
</style>
