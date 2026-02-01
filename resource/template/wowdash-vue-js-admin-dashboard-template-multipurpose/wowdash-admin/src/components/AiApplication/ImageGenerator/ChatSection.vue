<template>
    <div class="col-xxl-9 col-lg-8">
      <div class="chat-main card overflow-hidden">
        <!-- Header -->
        <div class="chat-sidebar-single gap-8 justify-content-between cursor-default flex-nowrap">
          <div class="d-flex align-items-center gap-16">
            <router-link to="/code-generator-new" class="text-primary-light text-2xl line-height-1">
              <i class="ri-arrow-left-line"></i>
            </router-link>
            <h6 class="text-lg mb-0 text-line-1">
              Please, Make 4 variant of this image Quickly As Soon As possible
            </h6>
          </div>
          <div class="d-flex align-items-center gap-16 flex-shrink-0">
            <button type="button" class="text-secondary-light text-xl line-height-1 text-hover-primary-600">
              <i class="ri-edit-2-line"></i>
            </button>
            <button type="button" class="text-secondary-light text-xl line-height-1 text-hover-primary-600">
              <i class="ri-delete-bin-6-line"></i>
            </button>
          </div>
        </div>
  
        <!-- Chat Messages -->
        <div class="chat-message-list max-h-612-px min-h-612-px">
          <div
            v-for="(item, index) in chatItems"
            :key="index"
            class="d-flex align-items-start gap-16 border-bottom border-neutral-200 pb-16 mb-16"
          >
            <div class="img overflow-hidden flex-shrink-0">
              <img :src="item.imgSrc" alt="image" class="w-44-px h-44-px rounded-circle object-fit-cover" />
            </div>
  
            <!-- TEXT -->
            <div
              v-if="item.type === 'text'"
              class="d-flex align-items-start justify-content-between flex-grow-1 gap-16"
            >
              <div class="info">
                <h6 class="text-lg mb-4">{{ item.name }}</h6>
                <p class="mb-0 text-secondary-light text-sm">{{ item.text }}</p>
              </div>
              <button
                type="button"
                class="d-flex align-items-center gap-6 px-8 py-4 bg-primary-50 radius-4 bg-hover-primary-100 flex-shrink-0"
              >
                <i class="ri-edit-2-fill"></i> Edit
              </button>
            </div>
  
            <!-- IMAGE -->
            <div v-else class="info flex-grow-1">
              <h6 class="text-lg mb-16 mt-8">{{ item.name }}</h6>
  
              <!-- Single Image -->
              <div v-if="item.images.length === 1" class="row g-3">
                <div class="col-sm-6">
                  <div class="generated-image-item radius-8 overflow-hidden position-relative border border-primary-600 border-width-2-px"
                  >
                    <img :src="item.images[0].src" :alt="item.images[0].alt" class="w-100 h-100 object-fit-cover" />
                    <button type="button" class="download-btn position-absolute top-0 end-0 me-8 mt-8 w-50-px h-50-px bg-primary-600 text-white d-flex justify-content-center align-items-center radius-6 text-2xl bg-hover-primary-700">
                        <i class="ri-download-2-fill"></i>
                    </button>
                  </div>
                </div>
              </div>
  
              <!-- Multiple Images -->
              <div v-else class="row g-3">
                <div
                  v-for="(image, imgIndex) in item.images"
                  :key="imgIndex"
                  class="col-xl-3 col-sm-6"
                >
                  <div
                    class="generated-image-item radius-8 overflow-hidden position-relative"
                    :class="{ 'border border-primary-600 border-width-2-px': selectedImages.includes(imgIndex) }"
                  >
                    <img :src="image.src" :alt="image.alt" class="w-100 h-100 object-fit-cover" />
                    <div
                      class="form-check style-check d-flex align-items-center position-absolute top-0 start-0 ms-8 mt-8"
                    >
                      <input
                        class="form-check-input radius-4 border border-neutral-400"
                        :id="'image' + imgIndex"
                        type="checkbox"
                        @click="toggleImage(imgIndex)"
                      />
                    </div>
                    <label
                      :for="'image' + imgIndex"
                      class="position-absolute start-0 top-0 w-100 h-100"
                    ></label>
                  </div>
                </div>
              <!-- Image Actions -->
              <div class="d-flex align-items-center gap-16 mt-24 flex-wrap">
                <button type="button" class="btn btn-outline-primary-600">🚀 Upscale (2x)</button>
                <button type="button" class="btn btn-outline-primary-600">🎲 Make Square</button>
                <button type="button" class="btn btn-outline-primary-600">⭐ Zoom Out 2x</button>
                <button type="button" class="btn btn-outline-primary-600">🎉️ Upscale (4x)</button>
                <button type="button" class="btn btn-outline-primary-600">🎁 Upscale (6x)</button>
              </div>
              </div>
  
  
              <!-- Footer Toolbar -->
              <div class="mt-24 d-flex align-items-center justify-content-between gap-16">
                <div class="d-flex align-items-center gap-20 bg-neutral-50 radius-8 px-16 py-10 line-height-1">
                  <button type="button" class="text-secondary-light text-2xl d-flex text-hover-info-600">
                    <i class="ri-thumb-up-line line-height-1"></i>
                  </button>
                  <button type="button" class="text-secondary-light text-2xl d-flex text-hover-info-600">
                    <i class="ri-thumb-down-line"></i>
                  </button>
                  <button type="button" class="text-secondary-light text-2xl d-flex text-hover-info-600">
                    <i class="ri-share-forward-line"></i>
                  </button>
                  <button type="button" class="text-secondary-light text-2xl d-flex text-hover-info-600">
                    <i class="ri-download-2-fill"></i>
                  </button>
                </div>
                <button type="button" class="btn btn-outline-primary d-flex align-items-center gap-8">
                  <i class="ri-repeat-2-line"></i> Regenerate
                </button>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Chat Message Input -->
        <form class="chat-message-box" @submit.prevent="sendMessage">
          <input type="text" v-model="chatMessage" name="chatMessage" placeholder="Message wowdash..." />
          <button
            type="submit"
            class="w-44-px h-44-px d-flex justify-content-center align-items-center radius-8 bg-primary-600 text-white bg-hover-primary-700 text-xl"
          >
            <iconify-icon icon="f7:paperplane"></iconify-icon>
          </button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import img1 from '@/assets/images/chatgpt/image-generator1.png'
  import img2 from '@/assets/images/chatgpt/image-generator2.png'
  import img3 from '@/assets/images/chatgpt/image-generator3.png'
  import img4 from '@/assets/images/chatgpt/image-generator4.png'
  import userImg from '@/assets/images/chat/1.png'
  import wowdashImg from '@/assets/images/wow-dash-favicon.png'
  
  export default {
    data() {
      return {
        chatMessage: '',
        selectedImages: [],
        chatItems: [
          {
            type: 'text',
            name: 'Adam Milner',
            imgSrc: userImg,
            text: 'Please, Make 4 variant of this image Quickly As Soon As possible'
          },
          {
            type: 'image',
            name: 'WowDash',
            imgSrc: wowdashImg,
            images: [
              { src: img1, alt: 'image 1' },
              { src: img2, alt: 'image 2' },
              { src: img3, alt: 'image 3' },
              { src: img4, alt: 'image 4' }
            ]
          },
          {
            type: 'text',
            name: 'Adam Milner',
            imgSrc: userImg,
            text: 'Please, Make 4 variant of this image Quickly As Soon As possible'
          },
          {
            type: 'image',
            name: 'WowDash',
            imgSrc: wowdashImg,
            images: [
              { src: img1, alt: 'image 1' }
            ]
          }
        ]
      };
    },
    methods: {
      toggleImage(index) {
        if (this.selectedImages.includes(index)) {
          this.selectedImages = this.selectedImages.filter(i => i !== index);
        } else {
          this.selectedImages.push(index);
        }
      },
      sendMessage() {
        if (this.chatMessage.trim()) {
          this.chatItems.push({
            type: 'text',
            name: 'You',
            imgSrc: userImg,
            text: this.chatMessage
          });
          this.chatMessage = '';
        }
      }
    }
  };
  </script>
  