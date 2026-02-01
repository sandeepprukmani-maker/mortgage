<template>
  <div class="dashboard-main-body">

    <Breadcrumb title="Text Generator" :breadcrumbs="[
      { name: 'Text Generator' }
    ]" />

    <div class="row gy-4 flex-wrap-reverse">

      <!-- Chat Sidebar -->
      <TextSidebar />
      <!-- Chat Area -->
      <NewChat />

    </div>
  </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import TextSidebar from '@/components/AiApplication/TextGenerator/TextSidebar.vue'
import NewChat from '@/components/AiApplication/TextGenerator/NewChat.vue'

export default {
  name: "TextGenerator",
  components: {
    Breadcrumb,
    TextSidebar,
    NewChat
  },
}
</script>