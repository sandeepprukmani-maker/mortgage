<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Pagination" :breadcrumbs="[
            { name: 'Components / Pagination' }
        ]" />

        <PaginationData />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import PaginationData from '@/components/UiComponent/PaginationData.vue'

export default {
    name: "Pagination",
    components: {
        Breadcrumb,
        PaginationData,
    },
}
</script>