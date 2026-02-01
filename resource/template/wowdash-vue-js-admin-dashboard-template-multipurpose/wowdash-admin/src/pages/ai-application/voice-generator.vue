<template>
  <div class="dashboard-main-body">
    <Breadcrumb title="Voice Generator" :breadcrumbs="[
      { name: 'Voice Generator' }
    ]" />

    <div class="row gy-4">
    <VoiceSidebar />
    <ChatSection />
  </div>
    
  </div>
</template>

<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import VoiceSidebar from '@/components/AiApplication/VoiceGenerator/VoiceSidebar.vue'
import ChatSection from '@/components/AiApplication/VoiceGenerator/ChatSection.vue'

export default {
  name: "TextGenerator",
  components: {
    Breadcrumb,
    VoiceSidebar,
    ChatSection
  },
}
</script>