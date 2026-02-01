<template>
    
    <div class="col-xxl-9 col-lg-8">
        <div class="chat-main card overflow-hidden">
          <div class="chat-sidebar-single gap-8 justify-content-between cursor-default flex-nowrap">
            <div class="d-flex align-items-center gap-16">
              <router-link to="/text-new-chat" class="text-primary-light text-2xl line-height-1">
                <i class="ri-arrow-left-line"></i>
              </router-link>
              <h6 class="text-lg mb-0 text-line-1">UI/UX Design Roadmap write me</h6>
            </div>

            <div class="d-flex align-items-center gap-16 flex-shrink-0">
              <button type="button" class="text-secondary-light text-xl line-height-1 text-hover-primary-600"><i
                  class="ri-edit-2-line"></i></button>
              <button type="button" class="text-secondary-light text-xl line-height-1 text-hover-primary-600"><i
                  class="ri-delete-bin-6-line"></i></button>
            </div>
          </div>

          <div class="chat-message-list max-h-612-px min-h-612-px">
            <template v-for="(message, index) in chatMessages" :key="index">
              <div v-if="!message.isBot"
                class="d-flex align-items-start justify-content-between gap-16 border-bottom border-neutral-200 pb-16 mb-16">
                <div class="d-flex align-items-center gap-16">
                  <div class="img overflow-hidden flex-shrink-0">
                    <img :src="message.userImage" alt="image" class="w-44-px h-44-px rounded-circle object-fit-cover">
                  </div>
                  <div class="info flex-grow-1">
                    <h6 class="text-lg mb-4">{{ message.userName }}</h6>
                    <p class="mb-0 text-secondary-light text-sm">{{ message.userText }}</p>
                  </div>
                </div>
                <button type="button"
                  class="d-flex align-items-center gap-6 px-8 py-4 bg-primary-50 radius-4 bg-hover-primary-100 flex-shrink-0">
                  <i class="ri-edit-2-fill"></i> Edit
                </button>
              </div>

              <div v-else class="d-flex align-items-start gap-16 border-bottom border-neutral-200 pb-16 mb-16">
                <div class="img overflow-hidden flex-shrink-0">
                  <img src="@/assets/images/wow-dash-favicon.png" alt="image"
                    class="w-44-px h-44-px rounded-circle object-fit-cover">
                </div>
                <div class="info flex-grow-1">
                  <h6 class="text-lg mb-16 mt-8">WowDash</h6>
                  <p class="mb-16 text-secondary-light text-sm">{{ message.botText }}</p>
                  <p class="fw-semibold text-primary-light my-16">1. Research and Discovery</p>
                  <p class="text-primary-light my-16">a. Understand the Business Goals</p>
                  <ul class="list-style">
                    <li class="text-primary-light m-0" v-for="(item, idx) in message.botPoints" :key="idx">
                      <span class="fw-semibold text-primary-light">{{ item.title }}:</span> {{ item.description }}
                    </li>
                  </ul>

                  <div class="mt-24 d-flex align-items-center justify-content-between gap-16">
                    <div class="d-flex align-items-center gap-20 bg-neutral-50 radius-8 px-16 py-10 line-height-1">
                      <button type="button" class="text-secondary-light text-2xl d-flex text-hover-info-600"><i
                          class="ri-thumb-up-line line-height-1"></i></button>
                      <button type="button" class="text-secondary-light text-2xl d-flex text-hover-info-600"><i
                          class="ri-thumb-down-line"></i></button>
                      <button type="button" class="text-secondary-light text-2xl d-flex text-hover-info-600"><i
                          class="ri-share-forward-line"></i></button>
                      <button type="button" class="text-secondary-light text-2xl d-flex text-hover-info-600"><i
                          class="ri-file-copy-line"></i></button>
                    </div>
                    <button type="button" class="btn btn-outline-primary d-flex align-items-center gap-8">
                      <i class="ri-repeat-2-line"></i> Regenerate
                    </button>
                  </div>
                </div>
              </div>
            </template>
          </div>

          <form class="chat-message-box" @submit.prevent="sendMessage">
            <input type="text" v-model="chatInput" name="chatMessage" placeholder="Message wowdash..." />
            <button type="submit"
              class="w-44-px h-44-px d-flex justify-content-center align-items-center radius-8 bg-primary-600 text-white bg-hover-primary-700 text-xl">
              <iconify-icon icon="f7:paperplane"></iconify-icon>
            </button>
          </form>
        </div>
      </div>
</template>
<script>
import chatUser from '@/assets/images/chat/1.png';
import user from '@/assets/images/wow-dash-favicon.png';

export default {
  data() {
    return {
      chatMessages: [
        {
          userImage: chatUser,
          userName: 'Adam Milner',
          userText: 'UI/UX Design Roadmap write me the roadmap right now',
          isBot: false,
        },
        {
          userImage: user,
          userName: 'WowDash',
          botText: 'Creating a UI/UX Design roadmap involves several key stages, from initial research to final testing and iteration. Here’s a detailed roadmap that outlines the typical steps and best practices in a UI/UX design project:',
          isBot: true,
          botPoints: [
            { title: 'Kickoff Meeting', description: 'Meet with stakeholders to understand the business objectives, target audience, and project scope.' },
            { title: 'Kickoff Meeting', description: 'Meet with stakeholders to understand the business objectives, target audience, and project scope.' }
          ]
        },
        {
          userImage: chatUser,
          userName: 'Adam Milner',
          userText: 'UI/UX Design Roadmap write me the roadmap right now',
          isBot: false,
        },
        {
          userImage: user,
          userName: 'WowDash',
          botText: 'Creating a UI/UX Design roadmap involves several key stages, from initial research to final testing and iteration. Here’s a detailed roadmap that outlines the typical steps and best practices in a UI/UX design project:',
          isBot: true,
          botPoints: [
            { title: 'Kickoff Meeting', description: 'Meet with stakeholders to understand the business objectives, target audience, and project scope.' },
            { title: 'Kickoff Meeting', description: 'Meet with stakeholders to understand the business objectives, target audience, and project scope.' }
          ]
        }
      ],
      chatInput: ''
    }
  },
  methods: {
    sendMessage() {
      if (this.chatInput.trim() !== '') {
        this.chatMessages.push({
          userImage: chat,
          userName: 'You',
          userText: this.chatInput,
          isBot: false
        });
        this.chatInput = '';
      }
    }
  }
}

</script>