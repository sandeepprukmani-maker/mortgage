<template>
  <div class="dashboard-main-body">
    <Breadcrumb title="Notification" :breadcrumbs="[
      { name: 'Setting -  Notification' }
    ]" />
    <Notification />
  </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import Notification from '@/components/Settings/Notification.vue'
export default {
  name: "NotificationForm",
  components: {
    Breadcrumb,
    Notification
  },
}
</script>