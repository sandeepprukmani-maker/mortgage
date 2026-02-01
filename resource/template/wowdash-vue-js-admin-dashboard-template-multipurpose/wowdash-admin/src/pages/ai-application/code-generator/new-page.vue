<template>
  <div class="dashboard-main-body">
    <Breadcrumb title="Code Generator" :breadcrumbs="[
      { name: 'Code Generator' }
    ]" />

    <div class="row gy-4 flex-wrap-reverse">
        <!-- Code Sidebar -->
        <CodeSidebar />
        <NewChat />
    </div>
  </div>
</template>

<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import CodeSidebar from '@/components/AiApplication/CodeGenerator/CodeSidebar.vue'
import NewChat from '@/components/AiApplication/CodeGenerator/NewChat.vue'

export default {
  name: "CodeGenerator",
  components: {
    Breadcrumb,
    CodeSidebar,
    NewChat
  },
}
</script>