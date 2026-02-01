<template>
  <div class="dashboard-main-body">

    <Breadcrumb title="Column Chart" :breadcrumbs="[
      { name: 'Components / Column Chart' }
    ]" />

    <div class="row gy-4">
      <ColumnOne />
      <ColumnTwo />
      <GroupColumn />
      <SimpleColumn />
    </div>

  </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import ColumnOne from '@/components/Chart/ColumnChart/ColumnOne.vue'
import ColumnTwo from '@/components/Chart/ColumnChart/ColumnTwo.vue'
import GroupColumn from '@/components/Chart/ColumnChart/GroupColumn.vue'
import SimpleColumn from '@/components/Chart/ColumnChart/SimpleColumn.vue'

export default {
  name: "ColumnChart",
  components: {
    Breadcrumb,
    ColumnOne,
    ColumnTwo,
    GroupColumn,
    SimpleColumn
  },
}
</script>