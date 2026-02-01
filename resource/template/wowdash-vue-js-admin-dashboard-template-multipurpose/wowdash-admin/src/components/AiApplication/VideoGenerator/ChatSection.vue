<template>
    <div class="col-xxl-9 col-lg-8">
      <div class="chat-main card overflow-hidden">
        <div class="chat-sidebar-single gap-8 justify-content-between cursor-default flex-nowrap">
          <div class="d-flex align-items-center gap-16">
            <router-link to="/text-new-chat" class="text-primary-light text-2xl line-height-1">
              <i class="ri-arrow-left-line"></i>
            </router-link>
            <h6 class="text-lg mb-0 text-line-1">Please, Make 4 variant of this image Quickly As Soon As possible</h6>
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
  
        <!-- Chat Message List -->
        <div class="chat-message-list max-h-612-px min-h-612-px">
          <div
            v-for="(item, index) in chatItems"
            :key="index"
            class="d-flex align-items-start gap-16 border-bottom border-neutral-200 pb-16 mb-16"
          >
            <div class="img overflow-hidden flex-shrink-0">
              <img :src="item.imgSrc" alt="image" class="w-44-px h-44-px rounded-circle object-fit-cover" />
            </div>
  
            <!-- TEXT MESSAGE -->
            <div v-if="item.type === 'text'" class="d-flex align-items-start justify-content-between flex-grow-1 gap-16">
              <div class="info">
                <h6 class="text-lg mb-4">{{ item.name }}</h6>
                <p class="mb-0 text-secondary-light text-sm">{{ item.text }}</p>
              </div>
              <button type="button" class="d-flex align-items-center gap-6 px-8 py-4 bg-primary-50 radius-4 bg-hover-primary-100 flex-shrink-0">
                <i class="ri-edit-2-fill"></i> Edit
              </button>
            </div>
  
            <!-- IMAGE MESSAGE -->
            <div v-else class="info flex-grow-1">
              <h6 class="text-lg mb-16 mt-8">{{ item.name }}</h6>
              <div class="row g-3">
                <div class="col-xl-4 col-sm-6">
                  <div class="generated-image-item radius-8 overflow-hidden position-relative">
                    <img :src="item.imageSrc" alt="" class="w-100 h-100 object-fit-cover" />
                    <button class="w-72-px h-72-px bg-primary-600 rounded-circle text-white text-2xxl d-flex align-items-center justify-content-center bg-hover-primary-700 position-absolute top-50 start-50 translate-middle">
                      <i class="ri-play-large-fill"></i>
                    </button>
                  </div>
                </div>
              </div>
              <button type="button" class="btn btn-primary d-flex align-items-center gap-8 px-20 flex-shrink-0 mt-16">
                Download
                <i class="ri-download-2-line"></i>
              </button>
  
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
                </div>
                <button type="button" class="btn btn-outline-primary d-flex align-items-center gap-8">
                  <i class="ri-repeat-2-line"></i> Regenerate
                </button>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Chat Message Box -->
        <form class="chat-message-box" @submit.prevent="sendMessage">
          <input type="text" v-model="newMessage" name="chatMessage" placeholder="Message wowdash..." />
          <button type="submit" class="w-44-px h-44-px d-flex justify-content-center align-items-center radius-8 bg-primary-600 text-white bg-hover-primary-700 text-xl">
            <iconify-icon icon="f7:paperplane"></iconify-icon>
          </button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import chatUser from '@/assets/images/chat/1.png'
  import favicon from '@/assets/images/wow-dash-favicon.png'
  import generatorImg from '@/assets/images/chatgpt/image-generator5.png'
  
  export default {
    data() {
      return {
        newMessage: '',
        chatItems: [
          {
            type: 'text',
            name: 'Adam Milner',
            imgSrc: chatUser,
            text: `Alright guys, so I've just seen this website, Fortunanest website, it's an investment website and you invest there. So I actually tried it some months, I tried it just for 3 months and I realized everything was working correct. I was thinking it was this fake website, I never met this website.`,
          },
          {
            type: 'image',
            name: 'WowDash',
            imgSrc: favicon,
            imageSrc: generatorImg,
          },
          {
            type: 'text',
            name: 'Adam Milner',
            imgSrc: chatUser,
            text: `Alright guys, so I've just seen this website, Fortunanest website, it's an investment website and you invest there. So I actually tried it some months, I tried it just for 3 months and I realized everything was working correct. I was thinking it was this fake website, I never met this website.`,
          },
          {
            type: 'image',
            name: 'WowDash',
            imgSrc: favicon,
            imageSrc: generatorImg,
          },
        ]
      };
    },
    methods: {
      sendMessage() {
        if (this.newMessage.trim()) {
          this.chatItems.push({
            type: 'text',
            name: 'You',
            imgSrc: chatUser,
            text: this.newMessage
          });
          this.newMessage = '';
        }
      }
    }
  };
  </script>
  