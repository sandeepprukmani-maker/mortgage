<template>
  <div class="dashboard-main-body">
    <Breadcrumb title="Text Generator" :breadcrumbs="[
      { name: 'Text Generator' }
    ]" />

    <div class="row gy-4 flex-wrap-reverse">

      <!-- Chat Sidebar -->
       <TextSidebar />
       <ChatSection />

    </div>
  </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import TextSidebar from '@/components/AiApplication/TextGenerator/TextSidebar.vue'
import ChatSection from '@/components/AiApplication/TextGenerator/ChatSection.vue'

export default {
  name: "TextGenerator",
  components: {
    Breadcrumb,
    TextSidebar,
    ChatSection
  },
}
</script>