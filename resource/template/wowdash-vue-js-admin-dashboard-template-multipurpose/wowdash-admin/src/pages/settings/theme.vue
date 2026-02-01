<template>
  <div class="dashboard-main-body">
    <Breadcrumb title="Theme" :breadcrumbs="[
      { name: 'Setting -  Theme' }
    ]" />

    <Theam />
  </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import Theam from '@/components/Settings/Theam.vue'
export default {
  name: "TheamData",
  components: {
    Breadcrumb,
    Theam
  },
}
</script>