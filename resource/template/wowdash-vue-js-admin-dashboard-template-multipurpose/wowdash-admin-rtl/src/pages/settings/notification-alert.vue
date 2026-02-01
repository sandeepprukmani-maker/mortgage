<template>
  <div class="dashboard-main-body">
    <Breadcrumb title="Notification Alert" :breadcrumbs="[
      { name: 'Setting -  Notification Alert' }
    ]" />

    <NotificationAlert />
  </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import NotificationAlert from '@/components/Settings/NotificationAlert.vue'
export default {
  name: "Notificationalert",
  components: {
    Breadcrumb,
    NotificationAlert
  },
}
</script>