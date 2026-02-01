<template>
  <div class="dashboard-main-body">
    <Breadcrumb title="Language" :breadcrumbs="[
      { name: 'Setting -  PaymentGateway' }
    ]" />

    <Payment />
  </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import Payment from '@/components/PaymentGateway/Payment.vue'
export default {
    name: "PaymentGateway",
    components: {
        Breadcrumb,
        Payment
    },
}
</script>