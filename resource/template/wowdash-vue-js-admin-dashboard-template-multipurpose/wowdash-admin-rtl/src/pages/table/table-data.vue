<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Data Table" :breadcrumbs="[
            { name: 'Data Table' }
        ]" />

        <DataTable />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import DataTable from '@/components/Table/DataTable.vue'

export default {
  name: "TableData",
  components: {
    Breadcrumb,
    DataTable,
  },
}
</script>