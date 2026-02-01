<template>
    <div class="card radius-16">
      <div class="card-header">
        <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
          <h6 class="mb-2 fw-bold text-lg mb-0">Quick Transfer</h6>
        </div>
      </div>
  
      <div class="card-body p-0">
        <div class="p-20">
          <div class="position-relative z-1 py-32 text-center px-3">
            <img
              src="@/assets/images/home-eleven/bg/bg-orange-gradient.png"
              alt=""
              class="position-absolute top-0 start-0 w-100 h-100 z-n1"
            />
            <h3 class="text-white">$500.00</h3>
            <span class="text-white">Your Balance</span>
          </div>
        </div>
  
        <div class="px-24 bg-neutral-100 border-bottom-0 py-20 dark-bg-neutral-200">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
            <h6 class="mb-2 fw-bold text-lg mb-0">Contacts</h6>
            <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
              View All
              <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
            </a>
          </div>
        </div>
  
        <div class="py-16 px-24">
          <div ref="slider" class="officer-slider d-flex overflow-hidden">
            <div
              v-for="(officer, index) in officers"
              :key="index"
              class="officer-slider__item d-flex flex-column text-center align-items-center justify-content-center"
            >
              <div class="officer-slider__thumb w-56-px h-56-px rounded-circle overflow-hidden flex-shrink-0 mx-8">
                <img :src="officer.img" alt="" class="w-100 h-100 object-fit-cover" />
              </div>
              <div class="officer-slider__content mt-24 min-w-max-content">
                <h6 class="mb-0 text-xl">{{ officer.name }}</h6>
                <span class="text-sm text-secondary-light">{{ officer.title }}</span>
              </div>
            </div>
          </div>
  
          <form action="#">
            <div>
              <label for="message" class="d-block fw-semibold text-primary-light mb-8">Write Short Description</label>
              <textarea class="form-control" id="message" rows="4" cols="50" placeholder="Enter a description..."></textarea>
            </div>
            <div class="mt-16">
              <label for="Amount" class="d-block fw-semibold text-primary-light mb-8">Amount</label>
              <div class="d-flex gap-16">
                <input type="text" id="Amount" class="form-control form-control-lg" placeholder="Ex: $200" />
                <button class="btn btn-primary-600 flex-shrink-0 d-flex align-items-center gap-2 px-32" type="submit">
                  Send <i class="ri-send-plane-fill"></i>
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import officer1 from '@/assets/images/home-eleven/officer-img1.png'
  import officer2 from '@/assets/images/home-eleven/officer-img2.png'
  import officer3 from '@/assets/images/home-eleven/officer-img3.png'
  import officer4 from '@/assets/images/home-eleven/officer-img4.png'
  import officer5 from '@/assets/images/home-eleven/officer-img5.png'
  export default {
    data() {
      return {
        officers: [
          {
            name: "Mr. Bin",
            title: "Insurance officer",
            img: officer1,
          },
          {
            name: "Mr. Robiul",
            title: "Insurance officer",
            img: officer2,
          },
          {
            name: "Mr. Deo",
            title: "Insurance officer",
            img: officer3,
          },
          {
            name: "Mr. Riad",
            title: "Insurance officer",
            img: officer4,
          },
          {
            name: "Mr. Alex",
            title: "Insurance officer",
            img: officer5,
          },
          {
            name: "Mr. John",
            title: "Insurance officer",
            img: officer2,
          },
        ],
        slideIndex: 0,
      };
    },
    mounted() {
      this.startSlider();
    },
    methods: {
      startSlider() {
        const totalSlides = this.officers.length;
        const visibleSlides = 5;
        const slider = this.$refs.slider;
  
        setInterval(() => {
          this.slideIndex = (this.slideIndex + 1) % totalSlides;
          const slideWidth = slider.children[0].offsetWidth;
          slider.scrollTo({
            left: slideWidth * this.slideIndex,
            behavior: "smooth",
          });
        }, 2000);
      },
    },
  };
  </script>
  
  <style scoped>
  .officer-slider {
    scroll-behavior: smooth;
    transition: transform 0.8s ease;
  }
  .officer-slider__item {
    flex: 0 0 auto;
  }
  </style>
  