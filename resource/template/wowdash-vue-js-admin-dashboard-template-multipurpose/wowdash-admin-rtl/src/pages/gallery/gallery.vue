<template>
    <div class="dashboard-main-body">
        <Breadcrumb title="Gallery Grid Desc" :breadcrumbs="[
            { name: 'Gallery Grid Desc' }
        ]" />

        <GridDesc />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import GridDesc from '@/components/Gallery/GalleryGridDesc.vue'
export default {
    name: "GalleryGridDesc",
    components: {
        Breadcrumb,
        GridDesc,
    },
}
</script>