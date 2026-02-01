<template>
    <div class="dashboard-main-body">


        <Breadcrumb title="Alerts" :breadcrumbs="[
            { name: 'Components / Alerts' }
        ]" />

        <Alerts />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import Alerts from '@/components/UiComponent/Alerts.vue'

export default {
    name: "Alert",
    components: {
        Breadcrumb,
        Alerts,
    },
}
</script>