<template>
  <div class="dashboard-main-body">
    <Breadcrumb title="Invoice List" :breadcrumbs="[
      { name: 'Invoice List' }
    ]" />

    <!-- Card -->
    <List />

  </div>
</template>

<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue'
import List from '@/components/invoice/List.vue'

export default {
  name: "InvoiceList",
  components: {
    Breadcrumb,
    List,
  },
};
</script>