<template>
  <div class="dashboard-main-body">
    <Breadcrumb title="Invoice List" :breadcrumbs="[
      { name: 'Invoice List' }
    ]" />
    <!-- invoive preview -->
         <Preview />
  </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import Preview from '@/components/invoice/Preview.vue'

export default {
  name: 'InvoicePreview',
  components: {
    Breadcrumb,
    Preview,
  }
}
</script>