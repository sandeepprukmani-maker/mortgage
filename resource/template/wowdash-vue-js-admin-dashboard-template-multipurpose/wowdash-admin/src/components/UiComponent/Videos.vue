<template>
    <div class="row gy-4">
      <!-- Default Video -->
      <div class="col-xxl-6">
        <div class="card h-100 p-0">
          <div class="card-header border-bottom bg-base py-16 px-24">
            <h6 class="text-lg fw-semibold mb-0">Default Video</h6>
          </div>
          <div class="card-body p-24">
            <div class="position-relative">
              <img
                src="@/assets/images/videos/video-img1.png"
                class="w-100 h-100 object-fit-cover radius-8"
                alt=""
              />
              <a
                @click.prevent="openVideoModal('https://www.youtube.com/watch?v=Vr9WoWXkKeE')"
                class="magnific-video bordered-shadow w-56-px h-56-px bg-white rounded-circle d-flex justify-content-center align-items-center position-absolute start-50 top-50 translate-middle z-1"
              >
                <iconify-icon icon="ion:play" class="text-primary-600 text-xxl"></iconify-icon>
              </a>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Videos With Content -->
      <div class="col-xxl-6">
        <div class="card h-100 p-0">
          <div class="card-header border-bottom bg-base py-16 px-24">
            <h6 class="text-lg fw-semibold mb-0">Videos With Content</h6>
          </div>
          <div class="card-body p-24">
            <div class="row gy-4">
              <div class="col-sm-6">
                <div class="border bg-base radius-8 overflow-hidden">
                  <div class="position-relative max-h-258-px overflow-hidden">
                    <img
                      src="@/assets/images/videos/video-img2.png"
                      class="w-100 object-fit-cover"
                      alt=""
                    />
                    <a
                      @click.prevent="openVideoModal('https://www.youtube.com/watch?v=Vr9WoWXkKeE')"
                      class="magnific-video bordered-shadow w-56-px h-56-px bg-white rounded-circle d-flex justify-content-center align-items-center position-absolute start-50 top-50 translate-middle z-1"
                    >
                      <iconify-icon icon="ion:play" class="text-primary-600 text-xxl"></iconify-icon>
                    </a>
                  </div>
                  <div class="p-16">
                    <h6 class="text-xl mb-6">This is Video title</h6>
                    <p class="text-secondary-light mb-0">
                      We quickly learn to fear and thus automatically avoid potentially stressful
                    </p>
                  </div>
                </div>
              </div>
              <div class="col-sm-6">
                <div class="border bg-base radius-8 overflow-hidden">
                  <div class="position-relative max-h-258-px overflow-hidden">
                    <img
                      src="@/assets/images/videos/video-img3.png"
                      class="w-100 object-fit-cover"
                      alt=""
                    />
                    <a
                      @click.prevent="openVideoModal('https://www.youtube.com/watch?v=Vr9WoWXkKeE')"
                      class="magnific-video bordered-shadow w-56-px h-56-px bg-white rounded-circle d-flex justify-content-center align-items-center position-absolute start-50 top-50 translate-middle z-1"
                    >
                      <iconify-icon icon="ion:play" class="text-primary-600 text-xxl"></iconify-icon>
                    </a>
                  </div>
                  <div class="p-16">
                    <h6 class="text-xl mb-6">This is Video title here</h6>
                    <p class="text-secondary-light mb-0">
                      We quickly learn to fear and thus automatically avoid potentially stressful
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Full-Width Video -->
      <div class="col-xxl-12">
        <div class="card h-100 p-0">
          <div class="card-header border-bottom bg-base py-16 px-24">
            <h6 class="text-lg fw-semibold mb-0">Video</h6>
          </div>
          <div class="card-body p-24">
            <div class="position-relative">
              <img
                src="@/assets/images/videos/video-img4.png"
                class="w-100 h-100 object-fit-cover radius-8"
                alt=""
              />
              <a
                @click.prevent="openVideoModal('https://www.youtube.com/watch?v=Vr9WoWXkKeE')"
                class="magnific-video bordered-shadow w-56-px h-56-px bg-white rounded-circle d-flex justify-content-center align-items-center position-absolute start-50 top-50 translate-middle z-1"
              >
                <iconify-icon icon="ion:play" class="text-primary-600 text-xxl"></iconify-icon>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  
    <!-- Video Modal -->
    <div
      v-if="isModalVisible"
      class="video-modal-overlay"
      @click.self="closeModal"
    >
      <div class="video-modal">
        <iframe
          :src="videoUrl"
          frameborder="0"
          allowfullscreen
          width="100%"
          height="100%"
        ></iframe>
        <button class="close-modal" @click="closeModal">Close</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        isModalVisible: false,
        videoUrl: "",
      };
    },
    methods: {
      openVideoModal(url) {
        this.videoUrl = `${url}?autoplay=1`;
        this.isModalVisible = true;
      },
      closeModal() {
        this.isModalVisible = false;
        this.videoUrl = "";
      },
    },
  };
  </script>
  
  <style scoped>
  .video-modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.7);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
  }
  
  .video-modal {
    position: relative;
    width: 80%;
    max-width: 890px;
    height: 53%;
    background-color: #000000;
    border-radius: 8px;
  }
  
  .close-modal {
    position: absolute;
    top: 10px;
    right: 10px;
    background: none;
    border: none;
    color: #333;
    font-size: 20px;
    cursor: pointer;
  }
  </style>
  