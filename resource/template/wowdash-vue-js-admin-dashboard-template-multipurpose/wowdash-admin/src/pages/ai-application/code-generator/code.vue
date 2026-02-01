<template>
  <div class="dashboard-main-body">
    <Breadcrumb title="Code Generator" :breadcrumbs="[
      { name: 'Code Generator' }
    ]" />

    <div class="row gy-4 flex-wrap-reverse">
        <!-- Code Sidebar -->
        <CodeSidebar />
        <ChatSection />
    </div>
  </div>
</template>

<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import CodeSidebar from '@/components/AiApplication/CodeGenerator/CodeSidebar.vue'
import ChatSection from '@/components/AiApplication/CodeGenerator/ChatSection.vue'

export default {
  name: "CodeGenerator",
  components: {
    Breadcrumb,
    CodeSidebar,
    ChatSection
  },
}
</script>