<template>
    <div class="col-xxl-9 col-lg-8">
        <div class="chat-main card overflow-hidden">

          <!-- Chat Topbar -->
          <div class="chat-sidebar-single gap-8 justify-content-between cursor-default flex-nowrap">
            <div class="d-flex align-items-center gap-16">
              <router-link to="/text-new-chat" class="text-primary-light text-2xl line-height-1">
                <i class="ri-arrow-left-line"></i>
              </router-link>
              <h6 class="text-lg mb-0 text-line-1">New Chat</h6>
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
          <div class="chat-message-list max-h-612-px min-h-612-px position-relative">
            <div v-if="chatMessages.length === 0"
              class="d-flex align-items-center justify-content-center flex-column h-100 position-absolute top-50 start-50 translate-middle">
              <img src="@/assets/images/chatgpt/empty-message-icon1.png" alt="Empty Chat" />
              <span class="text-secondary-light text-md mt-16">Type New Message</span>
            </div>

            <div v-else>
              <div v-for="(message, index) in chatMessages" :key="index" class="d-flex align-items-start gap-16 mb-16">
                <img :src="message.userImage" alt="User" class="w-44-px h-44-px rounded-circle object-fit-cover" />
                <div>
                  <h6 class="text-lg">{{ message.userName }}</h6>
                  <p class="text-secondary-light text-sm">{{ message.text }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Chat Input -->
          <form class="chat-message-box" @submit.prevent="sendMessage">
            <input type="text" v-model="newMessage" name="chatMessage" placeholder="Message wowdash..." />
            <button type="submit"
              class="w-44-px h-44-px d-flex justify-content-center align-items-center radius-8 bg-primary-600 text-white bg-hover-primary-700 text-xl">
              <iconify-icon icon="f7:paperplane"></iconify-icon>
            </button>
          </form>

        </div>
      </div>
</template>
<script>
import userImg from '@/assets/images/chatgpt/empty-message-icon1.png';

export default {
  data() {
    return {
      chatMessages: [],
      newMessage: '',
      userImage: userImg,
    };
  },
  methods: {
    sendMessage() {
      if (this.newMessage.trim() !== '') {
        this.chatMessages.push({
          userImage: this.userImage,
          userName: 'You',
          text: this.newMessage,
        });
        this.newMessage = '';
      }
    }
  }
};
</script>