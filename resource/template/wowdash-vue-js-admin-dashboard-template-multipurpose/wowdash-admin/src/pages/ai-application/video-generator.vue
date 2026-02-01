<template>
  <div class="dashboard-main-body">
    <Breadcrumb title="Image Generator" :breadcrumbs="[
      { name: 'Image Generator' }
    ]" />
    <div class="row gy-4">
      <VideoSidebar />
      <ChatSection />
    </div>
  </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import VideoSidebar from '@/components/AiApplication/VideoGenerator/VideoSidebar.vue'
import ChatSection from '@/components/AiApplication/VideoGenerator/ChatSection.vue'

export default {
  name: "TextGenerator",
  components: {
    Breadcrumb,
    VideoSidebar,
    ChatSection
  },
}
</script>