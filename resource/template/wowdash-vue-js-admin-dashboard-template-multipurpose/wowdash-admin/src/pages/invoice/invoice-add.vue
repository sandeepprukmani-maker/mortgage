<template>
  <div class="dashboard-main-body">
    <Breadcrumb title="Invoice List" :breadcrumbs="[
      { name: 'Invoice List' }
    ]" />

    <!-- Add Invoice -->
    <AddInvoice />
    
  </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue'
import AddInvoice from '@/components/invoice/AddInvoice.vue'

export default {
  name: "InvoiceAdd",
  components: {
    Breadcrumb,
    AddInvoice,
  },
};
</script>