<template>
    <div class="chat-sidebar card">
      <!-- Top Profile -->
      <div class="chat-sidebar-single active top-profile">
        <div class="img">
          <img src="@/assets/images/chat/1.png" alt="image" />
        </div>
        <div class="info">
          <h6 class="text-md mb-0">Kathryn Murphy</h6>
          <p class="mb-0">Available</p>
        </div>
        <div class="action">
          <div class="btn-group">
            <button type="button" class="text-secondary-light text-xl" data-bs-toggle="dropdown" data-bs-display="static" aria-expanded="false">
              <iconify-icon icon="bi:three-dots"></iconify-icon>
            </button>
            <ul class="dropdown-menu dropdown-menu-lg-end border">
              <li>
                <router-link
                  to="/chat-profile"
                  class="dropdown-item rounded text-secondary-light bg-hover-neutral-200 text-hover-neutral-900 d-flex align-items-center gap-2"
                >
                  <iconify-icon icon="fluent:person-32-regular"></iconify-icon>
                  Profile
                </router-link>
              </li>
              <li>
                <router-link
                  to="/chat-profile"
                  class="dropdown-item rounded text-secondary-light bg-hover-neutral-200 text-hover-neutral-900 d-flex align-items-center gap-2"
                >
                  <iconify-icon icon="carbon:settings"></iconify-icon>
                  Settings
                </router-link>
              </li>
            </ul>
          </div>
        </div>
      </div>
  
      <!-- Search -->
      <div class="chat-search">
        <span class="icon">
          <iconify-icon icon="iconoir:search"></iconify-icon>
        </span>
        <input type="text" v-model="searchQuery" autocomplete="off" placeholder="Search..." />
      </div>
  
      <!-- Chat List -->
      <div class="chat-all-list">
        <div
          v-for="(user, index) in filteredUsers"
          :key="index"
          class="chat-sidebar-single"
          :class="{ active: user.active }"
        >
          <div class="img">
            <img :src="user.image" :alt="user.name" />
          </div>
          <div class="info">
            <h6 class="text-sm mb-1">{{ user.name }}</h6>
            <p class="mb-0 text-xs">{{ user.message }}</p>
          </div>
          <div class="action text-end">
            <p class="mb-0 text-neutral-400 text-xs lh-1">{{ user.time }}</p>
            <span
              class="w-16-px h-16-px text-xs rounded-circle bg-warning-main text-white d-inline-flex align-items-center justify-content-center"
            >
              {{ user.unread }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import chatUser2 from "@/assets/images/chat/2.png"
  import chatUser3 from "@/assets/images/chat/3.png"
  import chatUser4 from "@/assets/images/chat/4.png"
  import chatUser5 from "@/assets/images/chat/5.png"
  import chatUser6 from "@/assets/images/chat/6.png"
  import chatUser7 from "@/assets/images/chat/7.png"
  import chatUser8 from "@/assets/images/chat/8.png"
  import chatUser9 from "@/assets/images/chat/9.png"
  import chatUser10 from "@/assets/images/chat/10.png"
  export default {
    name: "ChatSidebar",
    data() {
      return {
        searchQuery: "",
        users: [
          {
            name: "Kathryn Murphy",
            message: "hey! there i'm...",
            image: chatUser2,
            time: "12:30 PM",
            unread: 8,
            active: true,
          },
          {
            name: "James Michael",
            message: "hey! there i'm...",
            image: chatUser3,
            time: "12:30 PM",
            unread: 8,
            active: true,
          },
          {
            name: "Russell Lucas",
            message: "hey! there i'm...",
            image: chatUser4,
            time: "12:30 PM",
            unread: 8,
            active: false,
          },
          {
            name: "Caleb Bradley",
            message: "hey! there i'm...",
            image: chatUser5,
            time: "12:30 PM",
            unread: 8,
            active: false,
          },
          {
            name: "Bobby Roy",
            message: "hey! there i'm...",
            image: chatUser6,
            time: "12:30 PM",
            unread: 8,
            active: true,
          },
          {
            name: "Vincent Liam",
            message: "hey! there i'm...",
            image: chatUser7,
            time: "12:30 PM",
            unread: 8,
            active: true,
          },
          {
            name: "Randy Mason",
            message: "hey! there i'm...",
            image: chatUser8,
            time: "12:30 PM",
            unread: 8,
            active: true,
          },
          {
            name: "Albert Wayne",
            message: "hey! there i'm...",
            image: chatUser9,
            time: "12:30 PM",
            unread: 8,
            active: true,
          },
          {
            name: "Elijah Willie",
            message: "hey! there i'm...",
            image: chatUser10,
            time: "12:30 PM",
            unread: 8,
            active: true,
          },
          {
            name: "Kathryn Murphy",
            message: "hey! there i'm...",
            image: chatUser2,
            time: "12:30 PM",
            unread: 8,
            active: true,
          },
          {
            name: "James Michael",
            message: "hey! there i'm...",
            image: chatUser3,
            time: "12:30 PM",
            unread: 8,
            active: true,
          },
          {
            name: "Russell Lucas",
            message: "hey! there i'm...",
            image: chatUser4,
            time: "12:30 PM",
            unread: 8,
            active: false,
          },
          {
            name: "Caleb Bradley",
            message: "hey! there i'm...",
            image: chatUser5,
            time: "12:30 PM",
            unread: 8,
            active: false,
          },
          {
            name: "Bobby Roy",
            message: "hey! there i'm...",
            image: chatUser6,
            time: "12:30 PM",
            unread: 8,
            active: true,
          },
          {
            name: "Vincent Liam",
            message: "hey! there i'm...",
            image: chatUser7,
            time: "12:30 PM",
            unread: 8,
            active: true,
          },
          {
            name: "Randy Mason",
            message: "hey! there i'm...",
            image: chatUser8,
            time: "12:30 PM",
            unread: 8,
            active: true,
          },
          {
            name: "Albert Wayne",
            message: "hey! there i'm...",
            image: chatUser9,
            time: "12:30 PM",
            unread: 8,
            active: true,
          },
          {
            name: "Elijah Willie",
            message: "hey! there i'm...",
            image: chatUser10,
            time: "12:30 PM",
            unread: 8,
            active: true,
          },
        ],
      };
    },
    computed: {
      filteredUsers() {
        const query = this.searchQuery.toLowerCase();
        return this.users.filter((u) => u.name.toLowerCase().includes(query));
      },
    },
  };
  </script>
  