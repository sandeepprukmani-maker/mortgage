<template>
  <div class="dashboard-main-body">
    <Breadcrumb title="Chat" :breadcrumbs="[
      { name: 'Chat' }
    ]" />
    <div class="chat-wrapper">
      <ChatProfile />
      <ChatMessage />
    </div>

  </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import { Icon } from "@iconify/vue"; 
import ChatProfile from "@/components/chat/ChatProfile.vue"
import ChatMessage from "@/components/chat/ChatMessage.vue"

export default {
  name: "Chat",
  components: {
    Breadcrumb,
    Icon,
    ChatProfile,
    ChatMessage,
  },
};
</script>