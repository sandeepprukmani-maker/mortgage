<template>
  <div class="dashboard-main-body">
    <Breadcrumb title="Company" :breadcrumbs="[
      { name: 'Settings - Company' }
    ]" />
    <Company />
  </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import Company from '@/components/Settings/Company.vue'
export default {
  name: "CompanyForm",
  components: {
    Breadcrumb,
    Company
  },
}
</script>