<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="403" :breadcrumbs="[
            { name: '403' }
        ]" />

        <Forbidden />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import Forbidden from '@/components/Error/Forbidden.vue'
export default {
    name: "ForbiddenError",
    components: {
        Breadcrumb,
        Forbidden
    },
}
</script>