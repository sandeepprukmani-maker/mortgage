<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="View Profile" :breadcrumbs="[
            { name: 'View Profile' }
        ]" />

        <ViewProfiles />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import ViewProfiles from '@/components/Users/ViewProfile.vue'

export default {
  name: "ViewProfile",
  components: {
    Breadcrumb,
    ViewProfiles,
  },
}
</script>