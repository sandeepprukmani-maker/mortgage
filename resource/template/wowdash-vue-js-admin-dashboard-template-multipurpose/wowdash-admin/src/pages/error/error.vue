<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="400" :breadcrumbs="[
            { name: '400' }
        ]" />
        <PagenotFound />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import PagenotFound from '@/components/Error/PagenotFound.vue'
export default {
    name: "PagenotFoundError",
    components: {
        Breadcrumb,
        PagenotFound
    },
}
</script>