<template>
    <div class="chat-main card">
      <!-- Sidebar -->
      <div class="chat-sidebar-single active">
        <div class="img">
          <img :src="user.avatar" alt="image" />
        </div>
        <div class="info">
          <h6 class="text-md mb-0">{{ user.name }}</h6>
          <p class="mb-0">{{ user.status }}</p>
        </div>
        <div class="action d-inline-flex align-items-center gap-3">
          <button
            v-for="(action, index) in actionButtons"
            :key="index"
            type="button"
            class="text-xl text-primary-light"
          >
            <iconify-icon :icon="action.icon"></iconify-icon>
          </button>
          <div class="btn-group" v-if="menuAction">
            <button
              type="button"
              class="text-primary-light text-xl"
              data-bs-toggle="dropdown"
              data-bs-display="static"
              aria-expanded="false"
            >
              <iconify-icon icon="tabler:dots-vertical"></iconify-icon>
            </button>
            <ul class="dropdown-menu dropdown-menu-lg-end border">
              <li v-for="(option, idx) in menuAction.options" :key="idx">
                <button
                  class="dropdown-item rounded text-secondary-light bg-hover-neutral-200 text-hover-neutral-900 d-flex align-items-center gap-2"
                  type="button"
                >
                  <iconify-icon :icon="option.icon"></iconify-icon>
                  {{ option.label }}
                </button>
              </li>
            </ul>
          </div>
        </div>
      </div>
  
      <!-- Messages -->
      <div class="chat-message-list">
        <div
          v-for="(msg, index) in messages"
          :key="msg.id"
          :class="['chat-single-message', msg.side]"
        >
          <img
            v-if="msg.side === 'left'"
            :src="msg.avatar"
            alt="image"
            class="avatar-lg object-fit-cover rounded-circle"
          />
          <div class="chat-message-content">
            <p class="mb-3">{{ msg.text }}</p>
            <p class="chat-time mb-0">
              <span>{{ msg.time }}</span>
            </p>
          </div>
        </div>
      </div>
  
      <!-- Input Box -->
      <form class="chat-message-box" @submit.prevent="sendMessage">
        <input type="text" v-model="newMessage" placeholder="Write message" />
        <div class="chat-message-box-action">
          <button type="button" class="text-xl">
            <iconify-icon icon="ph:link"></iconify-icon>
          </button>
          <button type="button" class="text-xl">
            <iconify-icon icon="solar:gallery-linear"></iconify-icon>
          </button>
          <button
            type="submit"
            class="btn btn-sm btn-primary-600 radius-8 d-inline-flex align-items-center gap-1"
          >
            Send
            <iconify-icon icon="f7:paperplane"></iconify-icon>
          </button>
        </div>
      </form>
    </div>
  </template>
  
  <script>
  import chatUser from "@/assets/images/chat/11.png"
  export default {
    data() {
      return {
        user: {
          name: "Kathryn Murphy",
          status: "Available",
          avatar: chatUser
        },
        actionButtons: [
          { type: "call", icon: "mi:call" },
          { type: "video", icon: "fluent:video-32-regular" }
        ],
        menuAction: {
          type: "menu",
          options: [
            {
              label: "Clear All",
              icon: "mdi:clear-circle-outline",
              action: "clear"
            },
            {
              label: "Block",
              icon: "ic:baseline-block",
              action: "block"
            }
          ]
        },
        messages: [
          {
            id: 1,
            from: "Kathryn Murphy",
            side: "left",
            avatar: chatUser,
            text:
              "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters.",
            time: "6.30 pm"
          },
          {
            id: 2,
            from: "Me",
            side: "right",
            text:
              "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters.",
            time: "6.30 pm"
          },
          {
            id: 3,
            from: "Kathryn Murphy",
            side: "left",
            avatar: chatUser,
            text:
              "The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default.Contrary to popular belief, Lorem Ipsum is not simply random text is the model text for your company.",
            time: "6.30 pm"
          }
        ],
        newMessage: ""
      };
    },
    methods: {
      sendMessage() {
        if (this.newMessage.trim()) {
          this.messages.push({
            id: this.messages.length + 1,
            from: "Me",
            side: "right",
            text: this.newMessage.trim(),
            time: new Date().toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit"
            })
          });
          this.newMessage = "";
        }
      }
    }
  };
  </script>
  