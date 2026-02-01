<template>
  <div class="dashboard-main-body">
    <Breadcrumb title="Image Generator" :breadcrumbs="[
      { name: 'Image Generator' }
    ]" />

    <div class="row gy-4">
      <ImageSidebar />
      <ChatSection />
    </div>
  </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import ImageSidebar from '@/components/AiApplication/ImageGenerator/ImageSidebar.vue'
import ChatSection from '@/components/AiApplication/ImageGenerator/ChatSection.vue'

export default {
  name: "ImageGenerator",
  components: {
    Breadcrumb,
    ImageSidebar,
    ChatSection
  },
}
</script>