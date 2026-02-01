<template>
  <div class="dashboard-main-body">
    <Breadcrumb title="Invoice List" :breadcrumbs="[
      { name: 'Invoice Edit' }
    ]" />

    <!-- Edit Invoice -->
    <EditInvoice />
    
  </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue'
import EditInvoice from '@/components/invoice/Edit.vue'

export default {
  name: "InvoiceEdit",
  components: {
    Breadcrumb,
    EditInvoice,
  },
};
</script>