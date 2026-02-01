<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="503" :breadcrumbs="[
            { name: '503' }
        ]" />

        <ServiceUnavailable />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import ServiceUnavailable from '@/components/Error/ServiceUnavailable.vue'
export default {
    name: "ServiceUnavailableError",
    components: {
        Breadcrumb,
        ServiceUnavailable
    },
}
</script>